# Slide Deck (6 slides) — Speaker notes (short)

Slide 1: Title & Objective
- Quick context and goals for enterprise rollout.

Slide 2: Current State & Recap
- What the bot does today; constraints and assumptions.

Slide 3: Monitoring Stack (diagram)
- Explain JSON logs, Prometheus endpoint, Sentry for errors.
- Show sample metric chart and explain KPIs (latency, error rate, throughput).

Slide 4: Maintenance & Scaling Plan
- Patch workflow, Dependabot + pip-tools, GitHub Actions for CI/CD.
- Scaling steps for 5x/10x/100x with horizontal replicas and job sharding.

Slide 5: ROI Overview
- Present synthetic numbers, cost per transaction, labor saved.
- Decision justification and break-even estimate.

Slide 6: Risks & Mitigations / Next steps
- Alert fatigue, log storm, cost control, runbook snippets.
- Ask for questions.

(Export these to PPTX by copy/pasting into your slide tool; include screenshots from /diagrams.)
