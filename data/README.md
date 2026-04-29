### Data

This directory contains the evaluation data used in our experiments.

- `armarx_lt_mem/test-inc-qa.json` contains the real-world robot QA. The history trees are contained in the
  corresponding pickle files in that directory.
- `teach/interactive-v2` folder contains the QA evaluation sets used for the TEACh experiments. You need to get the
  full [TEACh data](https://github.com/alexa/teach/tree/main) to use this.

To reproduce our evaluation results, see the [runner scripts](../experiments/incremental).