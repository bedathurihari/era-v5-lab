# G5 local evidence — 26 Oct 2026

Local CPU smoke test on deterministic synthetic next-token sequences. This is not proof of KE2 integration or TSAI acceptance.

## Configuration checker

```text
Missing values / pending dependencies:
  PENDING: line 9: architecture.kronecker_pos_dim has no value
  PENDING: line 10: architecture.ke2_output_shape has no value
  PENDING: line 11: architecture.vocab_size has no value
  PENDING: line 12: architecture.hidden_size has no value
  PENDING: line 13: architecture.num_layers has no value
  PENDING: line 14: architecture.num_heads has no value
  PENDING: line 15: architecture.num_experts has no value
  PENDING: line 16: architecture.top_k has no value
  PENDING: line 17: architecture.max_context has no value
  PENDING: line 20: training.learning_rate has no value
  PENDING: line 21: training.batch_size has no value
  PENDING: line 22: training.steps has no value
Missing source / validation errors:
Errors: 0; pending: 12
```

Tiny config: `Errors: 0; pending: 0`.

## Train, same seed 1234 twice

```text
steps=20 first=3.855323 last=1.396178 finite=all
steps=20 first=3.855323 last=1.396178 finite=all
PASS: same seed, equal per-step loss, decreasing final loss
```

Number of compared steps: 20. First loss: 3.855323; final loss: 1.396178. Null metrics mean not measured, not zero.

Full machine-readable test outputs are in the local review bundle, not a new topic folder in the official team tree. Commands can be rerun using the included config.
