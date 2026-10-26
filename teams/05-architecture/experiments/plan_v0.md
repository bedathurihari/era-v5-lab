# G5 experimental plan v0 — DRAFT, pending TSAI approval

## Rules and controls
Run every arm with at least seeds 1234, 1235, 1236; match token budget, training/evaluation data, precision, logging, and hardware. Report mean and variation. All GPU hours below are **budgets/estimates, not observed runs**; revise after profiling. Do not copy V4 LR settings. Fix reference values only after local measurements and team consensus.

| Arm | Change from controlled baseline | Primary metric | Proposed pass bar | GPU-hours budget |
|---|---|---|---|---:|
| A0 | Tiny reference with deterministic seed | next-token CE loss and numerical stability | 0 NaN; exact seed-1234 CPU loss replay; decreasing loss | 0.25 |
| A1 | Sweep LR at 3 values centered on newly measured stable LR | held-out NTP loss | no divergence; candidate reduces held-out loss by >=1% vs A0 within matched tokens | 1.5 |
| A2 | Compare top-1 vs top-2 routing after compatible integration | loss vs tokens/s | candidate improves held-out CE by >=1% with <=15% throughput penalty | 1.5 |
| A3 | Compare dense FFN vs MoE at controlled active FLOPs | held-out loss / active FLOPs | improvement >=1% in held-out loss at matched compute | 2.0 |
| A4 | Kronecker reference embedding vs standard learned embedding (requires G4 interface) | held-out loss and input-embedding parameters | <=1% higher held-out loss with fewer input-embedding params | 2.0 |

**Total estimated budget: 7.25 GPU-hours.** Not measured; no approval implied.

## Dependencies
G4: KE2 output shape (27 Oct). G8: logger/alarms (29 Oct). TSAI: production size decisions (31 Oct). Current training harness uses a standard `nn.Embedding` and a top-1 router **only**; it is not falsely claimed to integrate KE2 or MTP. `loss_mtp` and `gpu_alloc_gb` are null if unavailable. Saturday review checks config/checker, repeatable loss, finite downward trend, and this experiment plan.
