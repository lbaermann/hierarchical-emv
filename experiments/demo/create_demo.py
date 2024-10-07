import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Union, Literal, Dict


@dataclass
class TreeNode:
    local_index: int
    dt_text: str
    text: str
    children: List[Union['TreeNode', Literal['hidden']]]

    def render_html(self, parent_stack=()):
        root = len(parent_stack) == 0
        icon_style = ('style="margin-left: 17px; height: 2px; width: 2px; margin-right:7px; border-width: 2px; '
                      'border-radius: 2px; background-color: gray"') if root else ''

        idx_stack = parent_stack + (self.local_index,)
        idx_str = '-'.join(map(str, idx_stack))
        leaf_cls = ' leaf' if len(self.children) == 0 else ''
        html_text = self.text.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        node = f'''
        <div class="node {leaf_cls}" id="node-{idx_str}">
            <i class="node-icon"{icon_style}></i>
            <i class="node-icon-2"></i>
            <p class="node-idx">{self.local_index}</p>
            <p class="node-dt">{self.dt_text}</p>
            <p class="node-summary">{html_text}</p>
        </div>'''
        if self.children:
            children = f'<div class="child-container l{len(parent_stack)}" id="child-container-{idx_str}">'
            children += f'''
            <div class="node-children-indicator" id="child-indicator-after-node-{idx_str}--1">
                <i class="node-icon"></i>
                <i class="fa-solid fa-ellipsis"></i>
            </div>
            '''  # Fake "after -1" => at index 0 child indicator
            for i, c in enumerate(self.children):
                if c == 'hidden':
                    pass
                    # children += f'''
                    # <div class="node-children-indicator" id="child-indicator-inside-node-{idx_str}-i{i}">
                    #    <i class="node-icon"></i>
                    #    <i class="fa-solid fa-ellipsis"></i>
                    # </div>
                    # '''
                else:
                    children += c.render_html(idx_stack)
            children += '</div>'
        else:
            children = ''

        if root:
            child_indicator = ''
        else:
            child_indicator = f'''
            <div class="node-children-indicator" id="child-indicator-after-node-{idx_str}">
                <i class="node-icon"></i>
                <i class="fa-solid fa-ellipsis"></i>
            </div>
            '''
        return node + children + child_indicator


def _create_tree_from_lines(tree_lines: List[str], tab_width=2):
    in_triple_quotes = False
    stack: List[Tuple[int, TreeNode]] = []
    for line in tree_lines:
        match = re.match(r'^\s*', line)
        num_spaces = len(match.group()) if match else 0
        depth = num_spaces // tab_width
        if depth > 0:
            while depth <= stack[-1][0]:
                stack.pop()

        match = re.match(r'(\d+: )?(?:([-0-9/: ]+): ("+)|SceneGraphInstant)', line.strip())
        if match:
            local_idx = int(match.group(1)[:-2]) if match.group(1) else 0  # for root node
            if match.group().endswith('SceneGraphInstant'):
                node = TreeNode(local_index=local_idx, dt_text='', text=line.strip()[match.end(1):].strip(),
                                children=[])
            else:
                node = TreeNode(local_index=local_idx, dt_text=match.group(2),
                                text=line.strip()[match.end():].strip('"'), children=[])
            if stack:  # stack is only empty for root node
                stack[-1][1].children.append(node)
            stack.append((depth, node))
            in_triple_quotes = match.group(3) == '"""'
        elif in_triple_quotes:
            end_str_idx = line.find('"""')
            end_str_idx = None if end_str_idx == -1 else end_str_idx
            if end_str_idx is not None:
                in_triple_quotes = False
            stack[-1][1].text += '\n  ' + line[:end_str_idx].strip(' "')
        elif line.strip(' "') == '...':
            assert depth == stack[-1][0] + 1
            stack[-1][1].children.append('hidden')

    return stack[0][1]


def _merge_trees(trees: List[TreeNode]):
    node = trees[0]
    if len(trees) == 1:
        return node

    assert all(
        t.local_index == node.local_index
        and t.text == node.text
        and t.dt_text == node.dt_text
        for t in trees
    ), f'All nodes should match (except their children): {trees}'

    new_node = TreeNode(node.local_index, node.dt_text, node.text, children=[])
    children_by_local_idx = defaultdict(list)
    final_hidden_after_local_idx_entries: List[int] = []
    for t in trees:
        for i, c in enumerate(t.children):
            if c != 'hidden':
                children_by_local_idx[c.local_index].append(c)
            elif i + 1 == len(t.children):
                final_hidden_after_local_idx_entries.append(
                    t.children[i - 1].local_index if i > 0 else 0
                )

    preliminary_children = []
    for children_for_one_idx in children_by_local_idx.values():
        preliminary_children.append(_merge_trees(children_for_one_idx))

    # Shortcut exit: If any of the input trees had no "hidden" child, there is no need to add any "hidden"
    if any(all(c != 'hidden' for c in t.children) for t in trees):
        preliminary_children.sort(key=lambda c: c.local_index)
        new_node.children = preliminary_children
        return new_node

    max_local_index = max((c.local_index for c in preliminary_children), default=0)
    children = new_node.children
    if preliminary_children:
        for i in range(max_local_index + 1):
            fitting_child = [c for c in preliminary_children if c.local_index == i]
            if fitting_child:
                children.append(fitting_child[0])
            elif len(children) == 0 or children[-1] != 'hidden':
                children.append('hidden')

    highest_idx_after_which_there_were_hidden_children = max(final_hidden_after_local_idx_entries, default=-1)
    if highest_idx_after_which_there_were_hidden_children >= max_local_index and (
            len(children) == 0 or children[-1] != 'hidden'):
        children.append('hidden')

    return new_node


def _read_messages_from_log(text_log: str):
    human = True
    messages = []
    for line in text_log.splitlines()[:-1]:
        if line.startswith('**'):
            human = 'Human' in line
            continue
        stripped_line = line.strip('" ')
        if stripped_line:
            messages.append((human, stripped_line))
    return messages


def load_steps_from_logfile(
        log_file: Path, sample_name: str
) -> List[Tuple[TreeNode, List[Tuple[bool, str]]]]:  # Tree, messages
    log = log_file.read_text()
    if 'Evaluating sample' in log:
        # Systematic eval mode
        log = log[log.find(f'Evaluating sample {sample_name}'):]
        log = '\n'.join(log.splitlines()[1:])
        log = log[:log.find('Evaluating sample')]
    else:
        # Live mode on robot
        assert 'Triggered question answering' in log
        log = log.split('Triggered question answering')[int(sample_name)]
    if 'Manual token count estimate' in log:
        request_parts = log.split('Manual token count estimate')
        skip_first_part = True
    else:
        request_parts = log.split('Updated/Defined variables after execution')
        skip_first_part = False
    steps = []
    print('Request parts:', len(request_parts))
    for i, part in enumerate(request_parts):
        if i == 0 and skip_first_part:
            continue  # First part is other output
        messages_start = part.find('"""User question: ') + len('"""User question: ')
        tree_start = part.find('"""Current state:') + len('"""Current state:\n')
        lines = part[tree_start:].splitlines()
        tree_end_idx = [i for i, line in enumerate(lines) if '{}' == line]
        if len(tree_end_idx) == 0:
            raise AssertionError(lines)
        tree_lines = lines[:tree_end_idx[0]]
        tree = _create_tree_from_lines(tree_lines)
        messages = _read_messages_from_log(part[messages_start:tree_start])
        steps.append((tree, messages))

    final_tree = steps[-1][0]
    last_msgs = steps[-1][1]

    if 'Answering' not in log:
        steps.append((final_tree, last_msgs + [(True, 'Error')]))
        return steps

    answer_start = log.find('Answering ') + len('Answering ')
    eval_answer_start = log.rfind('eval answer(') + len('eval ')
    answer_statement = log[eval_answer_start:log.find('\n', eval_answer_start)].strip()
    answer = log[answer_start:log.find('with reason:', answer_start)].strip()
    if len(last_msgs) == 1:
        # This must be the final try message.
        last_msgs = list(steps[-2][1])
        last_cmd_start = request_parts[-2].rfind('\neval ') + len('\neval ')
        last_msgs += [
            (False, request_parts[-2][last_cmd_start:request_parts[-2].find('\n', last_cmd_start)]),
            (True, 'Max rounds reached. Forcing answer now.')
        ]
        steps.pop()  # Pop the state that has only 1 message
        steps.append((final_tree, last_msgs))
    steps.append((final_tree, last_msgs + [(False, answer_statement)]))
    steps.append((final_tree, last_msgs + [(False, answer_statement), (True, answer)]))

    return steps


def _fill_states(merged_tree: TreeNode, tree_state: TreeNode, html_states: Dict[str, str], parent_stack=()):
    assert merged_tree.local_index == tree_state.local_index
    assert merged_tree.text == tree_state.text
    assert merged_tree.dt_text == tree_state.dt_text

    idx_stack = parent_stack + (merged_tree.local_index,)
    idx_str = '-'.join(map(str, idx_stack))

    visible_children_local_indices = [
        t.local_index for t in merged_tree.children
        if t != 'hidden' and any(s.local_index == t.local_index for s in tree_state.children if s != 'hidden')
    ]
    for v in visible_children_local_indices:
        html_states[f'node-{idx_str}-{v}'] = '-collapsed'
        html_states[f'child-container-{idx_str}-{v}'] = '-collapsed'

    for c in merged_tree.children:
        if c != 'hidden':
            s = [s for s in tree_state.children if s != 'hidden' and s.local_index == c.local_index]
            if s:
                # noinspection PyTypeChecker
                _fill_states(c, s[0], html_states, idx_stack)

    last_local_idx = max((c.local_index for c in merged_tree.children if c != 'hidden'), default=0)
    if len(visible_children_local_indices) == 0 and any(t != 'hidden' for t in merged_tree.children):
        # Shortcut to always use the child-indicator after the final node (animation looks better then)
        html_states[f'child-indicator-after-node-{idx_str}-{last_local_idx}'] = '+shown -collapsed'
        return

    last_visible_child = None
    last_hidden_indicator_idx = None
    for i in range(last_local_idx + 1):
        if i in visible_children_local_indices:
            last_visible_child = i
        else:
            if ((last_visible_child is None and last_hidden_indicator_idx is None)
                    or last_hidden_indicator_idx is None
                    or (last_visible_child is not None and last_visible_child > last_hidden_indicator_idx)):
                last_hidden_indicator_idx = i
                html_states[f'child-indicator-after-node-{idx_str}-{i - 1}'] = '+shown -collapsed'
    if merged_tree.children and merged_tree.children[-1] == 'hidden' and last_visible_child == last_local_idx:
        html_states[f'child-indicator-after-node-{idx_str}-{last_local_idx}'] = '+shown -collapsed'


def create_website_js_from_steps(merged_tree, steps) -> str:
    js_per_step = []

    for tree_state, messages in steps:
        states = {}
        _fill_states(merged_tree, tree_state, states)

        step_code = ''
        for element_id, state in states.items():
            element_code = f'$("#{element_id}")'
            for state_action in state.split():
                if '-' == state_action[0]:
                    element_code += f'.removeClass("{state_action[1:]}")'
                elif '+' == state_action[0]:
                    element_code += f'.addClass("{state_action[1:]}")'
            step_code += element_code + ';'
        step_code += ';'.join(f'$("#msg-{i}").removeClass("collapsed")' for i in range(len(messages)))
        js_per_step.append(step_code)

    apply_step_code = ''
    for i, code in enumerate(js_per_step):
        apply_step_code += f'if (step == {i}) ' + '{' + code + '}\n'
    return '''
    var step = 0;
    const numSteps = {num_steps};
    function applyStep() {
      $(".node").addClass("collapsed");
      $(".child-container").addClass("collapsed");
      $(".node-children-indicator").addClass("collapsed").removeClass("shown");
      $(".message").addClass("collapsed");
      $("#node-0, #child-container-0").removeClass("collapsed");
        
      {apply_step_code}
    }

    $("#button-prev").on("click", () => {
        if (step > 0) step -= 1;
        applyStep();
    })
    $("#button-next").on("click", () => {
        if (step + 1 < numSteps) step += 1;
        applyStep();
    })
    function animateStep() {
        $('#button-bar').css({'display': 'none'})
        setTimeout(() => {
            if (step + 1 < numSteps) {
                step += 1;
                applyStep();
                /*var leftCol = $('.column-left').get(0);
                leftCol.scrollTo({top: leftCol.scrollHeight, behavior: 'smooth'});*/
                animateStep();
            } else {
                $('#button-bar').css({'display': 'unset'})
            }
        }, 2000)
    }
    $("#button-animate").on("click", () => {
        step = 0;
        animateStep();
    })
    applyStep();
    
    function keyPress(e) {
        if(e.key === 'a') {
            $('#button-animate').click();
        }
    }
    document.addEventListener("keydown", keyPress, false);

    '''.replace('{apply_step_code}', apply_step_code).replace('{num_steps}', str(len(steps)))


def _create_html_from_messages(messages: List[Tuple[bool, str]]):
    initial_question = messages[0][1]
    assert messages[0][0], 'Initial message must be user question.'

    html_content = f'<div class="message initial" id="msg-0">{initial_question}</div>\n'
    for i, (is_human, text) in enumerate(messages):
        if i == 0 or i == len(messages) - 1:
            continue
        message_class = 'from-human' if is_human else 'from-bot'
        html_content += f'<div class="message {message_class}" id="msg-{i}">{text}</div>\n'

    answer = messages[-1][1]
    html_content += f'<div class="message answer" id="msg-{len(messages) - 1}">{answer}</div>\n'
    return html_content


def create_demo_from_logfile(log_file: Path, sample_name: str):
    steps = load_steps_from_logfile(log_file, sample_name)
    tree_per_step = [s[0] for s in steps]
    merged_tree = _merge_trees(tree_per_step)

    button_script = create_website_js_from_steps(merged_tree, steps)

    demo_dir = Path(__file__).parent
    template = (demo_dir / 'demo_template.html').read_text()
    output = (template
              .replace('{tree}', merged_tree.render_html())
              .replace('/*js_code*/', button_script)
              .replace('{messages}', _create_html_from_messages(steps[-1][1])))
    file_sample_name = sample_name if len(sample_name) < 200 else sample_name[:97] + '___' + sample_name[-100:]
    (demo_dir / f'{log_file.stem}-{file_sample_name}.html').write_text(output)


def main():
    log_file = Path(sys.argv[1])
    sample_or_json = sys.argv[2]
    if len(sample_or_json) < 200 and Path(sample_or_json).is_file():
        json_content = json.loads(Path(sample_or_json).read_text())
        samples = json_content['results'].keys()
        for sample in samples:
            create_demo_from_logfile(log_file, sample_name=sample)
    else:
        create_demo_from_logfile(log_file, sample_name=sample_or_json)


if __name__ == '__main__':
    main()
