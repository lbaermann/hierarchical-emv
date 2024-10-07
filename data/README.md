### Data

This directory contains the evaluation data used in our experiments.

- `armarx_lt_mem/qa.json` contains the real-world robot QA. The history tree is contained in the corresponding pickle
  files in that directory.
- `ego4d_long_qa/qa.json` contains the QA data for the Ego4D questions on extremely long videos, referring to Ego4D
  video UIDs. You need to get [Ego4D](https://ego4d-data.org) for using this.
- `teach` folder contains pickle files with the QA evaluation sets used for the TEACh experiments. You need to get the
  full [TEACh data](https://github.com/alexa/teach/tree/main) to use this.

To reproduce our evaluation results, see [llm_emv.eval](../llm_emv/eval/__main__.py).