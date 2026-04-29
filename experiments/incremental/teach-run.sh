base_args=(
  python -m llm_emv.eval.interactive
  --teach-base-dir ~/emv/data/TEACh/
  --dataset-file data/teach/interactive-v2/val-unseen-5.json
  --max-running-experiments 1
  --output-dir "output/interactive/$2"
)

local_llm="{'type':'ChatOpenAI', 'base_url':'http://localhost:8000/v1', 'openai_api_key':'fake', 'model':'meta-llama/Llama-3.3-70B-Instruct', 'temperature': 0, 'request_timeout': 90}"
remote_llm="{'type':'ChatOpenAI', 'model':'gpt-4.1-2025-04-14', 'temperature': 0, 'request_timeout': 60}"
feedback="file"

lang_rule_feedback_args=(
  --feedback-type "$feedback"
  --language-rule-mod-llm "$remote_llm"
  --feedback-llm "$local_llm"
)

relevance_args=(
  --language-rule-llm "$local_llm"
  --language-rule-mod-llm "$remote_llm"
  --feedback-llm "$local_llm"
)

offline_args=(
  --cfg teach/paper
  --dataset-type teach-full
  --llm-summarizer
  "{'llm': $local_llm, 'example_db_name': 'teach', 'few_shot_k': 2}"
)

flat_args=(
  --cfg teach/flat
  --dataset-type teach-scene
  --history-builder-llm "None"
  --history-builder-kwargs "{'flat': True}"
)

offline_forgetting_args=(
  --forgetting-kwargs "{}"
)

online_args=(
  --cfg teach/paper
  --dataset-type teach-scene
  --history-builder-llm "$local_llm"
)

case $1 in
# incremental
a) # full system
  "${base_args[@]}" "${online_args[@]}" "${relevance_args[@]}" --feedback-type $feedback
  ;;
a2) # no feedback for summarization (but for forgetting)
  "${base_args[@]}" "${online_args[@]}" "${relevance_args[@]}" --feedback-type $feedback --history-builder-kwargs "{'apply_rules_for_summarization': False}"
  ;;
b) # no feedback learning
  "${base_args[@]}" "${online_args[@]}" "${relevance_args[@]}" --feedback-type none
  ;;
c) # no relevance estimation (only time-based decay), with feedback for summary
  "${base_args[@]}" "${online_args[@]}" --language-rule-llm None "${lang_rule_feedback_args[@]}"
  ;;
d) # no relevance estimation (only time-based decay), no feedback
  "${base_args[@]}" "${online_args[@]}" --language-rule-llm None --feedback-type none
  ;;
e) # no forgetting, with feedback for summary
  "${base_args[@]}" "${online_args[@]}" --forgetting-kwargs None "${lang_rule_feedback_args[@]}"
  ;;
f) # baseline (only incremental tree building, no forgetting or feedback)
  "${base_args[@]}" "${online_args[@]}" --forgetting-kwargs None --feedback-type none
  ;;

# offline
g) # non-incremental but with all other options
  "${base_args[@]}" "${offline_args[@]}" "${relevance_args[@]}" "${offline_forgetting_args[@]}" --feedback-type $feedback
  ;;
h) # no feedback learning
  "${base_args[@]}" "${offline_args[@]}" "${relevance_args[@]}" "${offline_forgetting_args[@]}" --feedback-type none
  ;;
i) # only time-based decay, no learning
  "${base_args[@]}" "${offline_args[@]}" "${offline_forgetting_args[@]}" --feedback-type none
  ;;
j) # previous system (offline, no forgetting, no feedback)
  "${base_args[@]}" "${offline_args[@]}" --forgetting-kwargs None --feedback-type none
  ;;

# flat
k) # flat with forgetting and learning
  "${base_args[@]}" "${flat_args[@]}" "${relevance_args[@]}" --feedback-type $feedback
  ;;
l) # flat baseline
  "${base_args[@]}" "${flat_args[@]}" --forgetting-kwargs None --feedback-type none
  ;;

esac

