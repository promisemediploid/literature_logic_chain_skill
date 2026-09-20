# Design reference distilled from the user's example

The example emphasizes a full causal chain rather than a section summary. Its most useful patterns are:

- Start from the research problem and explain why prior approaches fail under the target setting.
- Identify one key conceptual observation, then show how it is operationalized as a learning signal.
- For each encoder/model, state its information role, not just its name.
- Treat frozen/trainable status as a causal design choice.
- Explain data construction decisions as confounder control or signal isolation.
- Treat the decoder/objective as a mechanism that forces the desired representation to be useful.
- Separate representation learning from downstream detection.
- Explain why few-shot and zero-shot are different inference settings when both exist.
- Read ablations as counterfactual evidence for design choices.
- Distinguish what the paper demonstrates from what remains unverified.
- Compress the entire argument into a final arrow chain.

The target reading style is: “problem → failure → hypothesis → operationalization → data → architecture → constraints → objective → representation → downstream use → evidence → ablation → limitation”.
