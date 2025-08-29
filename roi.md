# ROI Model (example, synthetic numbers)

## Inputs / Assumptions
- Current daily transactions (batches): 10,000 batches/day
- Average items per batch: 50
- Baseline human-handled time per batch: 2 minutes (manual intervention for exceptions)
- Cost of operator: $30/hour
- CPU cost estimate (cloud): $0.0005 per CPU-second
- Error rate: 0.5% currently, goal <0.1% with monitoring & recovery

## Calculations (sample)
- Labor minutes saved per day = batches * manual_minutes_saved_per_batch
- Cost per transaction = (CPU_seconds * cpu_unit_cost) + estimated SRE overhead
- Downtime avoided: modeled as hours/month avoided from faster MTTR

## Example outputs (synthetic)
- Labor saved: 10,000 * 2 min = 20,000 minutes/day → ~333 hours/day → $9,990/day (this is a hypothetical baseline)
- With automation and monitoring, assume 80% reduction in manual touches → $$7,992/day saved
- Cost to scale infra for 10×: incremental CPU cost ~ $300/day → ROI highly positive

(See notebooks or spreadsheets for full, reproducible calculations included in repo.)
