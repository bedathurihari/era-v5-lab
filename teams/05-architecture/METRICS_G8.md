# Proposed G8 metric contract — confirm at team sync

- `tokens_per_second`: wall-clock useful target tokens / training step seconds, volatile, not part of deterministic diff.
- `loss_ntp`: next-token cross-entropy scalar (real measured value).
- `loss_mtp`: future multi-token prediction loss; null until implemented, never fabricated.
- `loss`: total optimization loss (measured NTP-only in the current harness).
- `lr`: optimizer learning rate per step.
- `gpu_alloc_gb`: CUDA allocated memory in GB; null in CPU runs.

For identical-run comparisons, diff `step`, `loss_ntp`, `loss` and `lr`, NOT elapsed time or throughput.
