## Episodic Memory Verbalization using Hierarchical Representations of Life-Long Robot Experience

Abstract:

> Verbalization of robot experience, i.e., summarization of and question answering about a robot's past, is a crucial
> ability for improving human-robot interaction. Previous works applied rule-based systems or fine-tuned deep models to
> verbalize short (several-minute-long) streams of episodic data, limiting generalization and transferability. In our
> work, we apply large pretrained models to tackle this task with zero or few examples, and specifically focus on
> verbalizing life-long experiences. For this, we derive a tree-like data structure from episodic memory (EM), with
> lower
> levels representing raw perception and proprioception data, and higher levels abstracting events to natural language
> concepts. Given such a hierarchical representation built from the experience stream, we apply a large language model
> as
> an agent to interactively search the EM given a user's query, dynamically expanding (initially collapsed) tree nodes
> to
> find the relevant information. The approach keeps computational costs low even when scaling to months of robot
> experience data. We evaluate our method on simulated household robot data, human egocentric videos, and real-world
> robot
> recordings, demonstrating its flexibility and scalability.

For more details, see the [paper](https://arxiv.org/abs/2409.17702) and
our [website](https://hierarchical-emv.github.io), where you can also find demo videos and interactive results.

This repository contains the code and [data](data) used for the experiments in our paper.
You can also find the detailed evaluation results in `experiments/results`.


To reproduce the experimental results:

1. Set up the virtual environment (Python 3.10) using `pip install -r requirements.txt`
2. Make sure that the environment variable `OPENAI_API_KEY` is set appropriately
3. Run `python -m llm_emv.eval --help` to see the relevant parameters for the evaluation script. After choosing a
   `--dataset`, further parameters will appear (e.g. to set the download directory of Ego4D or TEACh). 

To interactively use H-EMV, try `python -m llm_emv --config armarx_lt_mem/full`