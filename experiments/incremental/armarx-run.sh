output_dir="output/interactive/armarx-v1/run-$1"
mkdir "$output_dir"

base_args=(
  python -m llm_emv.eval.interactive
  --pkl-base-dir ~/emv/data/physical/armem/preprocessed
  --qa-file "data/armarx_lt_mem/test-inc-qa.json"
  --cfg armarx_lt_mem/paper
  #--n-samples 2
  --max-running-experiments 10
  --max-loaded-experiments 10
  --max-parallel-qa-per-history 3
  --output-dir "$output_dir"
  --dataset-type armarx
)

local_llm="{'type':'ChatOpenAI', 'base_url':'http://localhost:8000/v1', 'openai_api_key':'fake', 'model':'meta-llama/Llama-3.3-70B-Instruct', 'temperature': 0, 'request_timeout': 180, 'max_tokens': 512}"
remote_llm="{'type':'ChatOpenAI', 'model':'gpt-5-2025-08-07', 'temperature': 0, 'request_timeout': 80}"
feedback="auto-always"

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
  --offline-summarizer-args
  "{'llm': $local_llm, 'example_db_name': 'armarx_lt_mem', 'few_shot_k': 2}"
)

offline_forgetting_args=(
  --forgetting-kwargs "{}"
)

online_args=(
  --online-builder-args "{'llm': $local_llm, 'action_param_summarizer_llm': $local_llm}" #'similarity_model_device': 'cuda:1'}"
  --offline-summarizer-args None
  --log-every-n-steps 10
)

case $1 in
# incremental
a) # full system
  "${base_args[@]}" "${online_args[@]}" "${relevance_args[@]}" --feedback-type $feedback
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
esac

