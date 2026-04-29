## Learning to Forget – Hierarchical Episodic Memory for Lifelong Robot Deployment

Abstract:

> Robots must verbalize their past experiences when users ask "Where did you put my keys?" or "Why did the task fail?"
> Yet maintaining life-long episodic memory (EM) from continuous multimodal perception quickly exceeds storage limits
> and makes real-time query impractical, calling for selective forgetting that adapts to users’ notions of relevance.
> We present H²-EMV, an online hierarchical EM framework that learns what to retain and what to discard from user
> feedback, featuring: (1) Online memory construction, updating EM incrementally as observations arrive; (2)
> Relevance‑based forgetting, where each node receives a default lifetime and an LLM‑based relevance estimator decides
> whether to retain or discard expired memories; (3) Feedback-based relevance learning, refining the relevance measure
> continuously from user feedback on forgotten details. Evaluations on simulated household tasks and real‑world
> recordings from the humanoid robot ARMAR‑7 demonstrate that H²-EMV maintains question‑answering accuracy while
> substantially reducing memory size and query‑time compute, with performance improving over time through relevance
> learning.

For more details, see the [paper](https://arxiv.org/abs/2604.11306).

Details about the underlying H-EMV method can be found on the [H-EMV website](https://hierarchical-emv.github.io) and on
its GitHub [branch](https://github.com/lbaermann/hierarchical-emv).

This branch contains the code and [data](data) used for the experiments in the H²-EMV paper.
You can also find the detailed evaluation results in `experiments/incremental/results`.

To reproduce the experimental results:

1. Set up the virtual environment (Python 3.10) using `pip install -r requirements.txt`
2. Make sure that the environment variable `OPENAI_API_KEY` is set appropriately. Also, some experiments use a local
   LLM, for which we used VLLM to host `meta-llama/Llama-3.3-70B-Instruct`.
3. Run `experiments/incremental/teach-run.sh` or `experiments/incremental/armarx-run.sh`. The different
   ablations/baselines are specified by the first parameters (a, b, c etc.). Adjust the parameters in these scripts as
   necessary.

The live deployment server can be found at `em/organize/history_server.py`.
