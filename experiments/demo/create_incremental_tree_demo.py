import sys
from copy import copy
from pathlib import Path
from typing import List, Tuple

from create_demo import TreeNode, create_tree_from_lines
from experiments.demo.create_demo import WEBSITE_JS_TEMPLATE


def _simplify_tree(node):
    if not isinstance(node, TreeNode):
        return node
    shallow_copy = copy(node)
    children = node.children
    while len(children) == 1 and isinstance(children[0], TreeNode) and node.text == children[0].text:
        children = children[0].children
    shallow_copy.children = [
        _simplify_tree(c)
        for c in children
    ]
    return shallow_copy


def load_incremental_tree_steps_from_logfile(
        log_file: Path
) -> List[Tuple[TreeNode, str]]:  # Tree, message (= newest item added to the tree)
    log = log_file.read_text()
    state_logs = log.split('=== Tree Update ===')[1:]
    steps = []
    print('State logs:', len(state_logs))
    for i, part in enumerate(state_logs):
        msg_start = part.find('=> Next item:') + len(' => Next item:')
        tree_start = part.find('=> Tree:') + len('=> Tree:\n')
        lines = part[tree_start:].splitlines()
        tree_end_idx = [j for j, line in enumerate(lines) if 'End Tree' == line]
        if len(tree_end_idx) == 0:
            print('Skipping!', i, part)
            break
            # raise AssertionError(lines)
        tree_lines = lines[:tree_end_idx[0]]
        tree = create_tree_from_lines(tree_lines)
        tree = _simplify_tree(tree)
        message = part[msg_start:part.find('\n', msg_start)].strip()
        steps.append((tree, message))

    return steps


def _create_html_from_message(messages: List[str]):
    html_content = ''
    for i, text in enumerate(messages):
        html_content += f'<div class="message from-human" id="msg-{i}">{text}</div>\n'
    return html_content


def _create_js(steps: List[Tuple[TreeNode, str]]):
    js_per_step = []
    for i, (tree, msg) in enumerate(steps):
        step_code = f'''
        $("#tree-container").html(`{tree.render_html()}`);
        $(".node-children-indicator").addClass("collapsed").removeClass("shown");
        $(".node").removeClass("collapsed"); 
        $(".child-container").removeClass("collapsed");
        ''' + '''
        $('.node').click((ev) => {
            let clickedId = ev.target.id;
            let nodeNumber = clickedId.substring('node-'.length)
            let childContainerId = `#child-container-${nodeNumber}`
            $(childContainerId).toggleClass('collapsed')
        })
        '''
        step_code += ';'.join(f'$("#msg-{j}").removeClass("collapsed")' for j in range(i + 1))
        js_per_step.append(step_code)

    apply_step_code = ''
    for i, code in enumerate(js_per_step):
        apply_step_code += f'if (step == {i}) ' + '{' + code + '}\n'

    return WEBSITE_JS_TEMPLATE.replace('{apply_step_code}', apply_step_code
                                       ).replace('{num_steps}', str(len(steps)))


def create_incremental_tree_demo_from_logfile(log_file: Path):
    steps = load_incremental_tree_steps_from_logfile(log_file)
    print(len(steps))
    print(len(steps))
    messages = [s[1] for s in steps]

    scripts = _create_js(steps)
    scripts += '''
    var style = document.createElement('style');
    style.append('.message, .node-children-indicator, .node { transition: none !important; }')
    style.append('.collapsed { display: none; }')
    style.append('.node-dt { pointer-events: none }')
    document.head.append(style)
    '''

    demo_dir = Path(__file__).parent
    template = (demo_dir / 'demo_template.html').read_text()
    output = (template
              .replace('{tree}', '<div id="tree-container"></div>')
              .replace('/*js_code*/', scripts)
              .replace('{messages}', _create_html_from_message(messages)))
    (demo_dir / f'{log_file.stem}.html').write_text(output)


def main():
    log_file = Path(sys.argv[1])
    create_incremental_tree_demo_from_logfile(log_file)


if __name__ == '__main__':
    main()
