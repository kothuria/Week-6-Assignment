# Monitoring Plan (one-page outline)

## Goals
- Provide deterministic telemetry for bot batches and resource usage
- Detect and alert on errors, latency regressions, retry storms, and resource exhaustion
- Allow rapid triage at 2 AM with structured logs + metrics + traces

## Telemetry emitted
- **Structured JSON logs** (rotated daily) with fields: timestamp, level, component, req_id, batch_id, duration_ms, status, error_code, message
- **Prometheus metrics endpoint** (HTTP /metrics) exporting:
  - inventory_batch_duration_seconds (histogram)
  - inventory_batch_success_total (counter)
  - inventory_batch_failures_total (counter, labeled by error)
  - inventory_processed_items_total (counter)
  - system_cpu_percent (gauge), system_memory_percent (gauge)
  - worker_active_replicas (gauge)
- **Error events** sent to Sentry (optional) for stacktraces and slow-failure grouping

## Storage & Access
- Logs written to rotating files in `/var/log/inventory-bot/` as JSON (also shipped to central storage in production)
- Metrics exposed via `prometheus_client` on port 9100 for scraping
- Synthetic "dashboard" scripts in `/scripts/` query Prometheus API to produce PNG plots for slides

## Visualization & Alerting (code-driven)
- Alerts are simulated by a small `scripts/alerting.py` that queries metrics and triggers webhooks 
- In real deployment: Alertmanager + PagerDuty / Slack integration
- Visualized via generated PNGs (scripts/visualize_metrics.py) and screenshots for the slide deck

## KPIs to track
- Mean batch latency (p50, p95, p99)
- Throughput (items/sec per replica)
- Error rate (%) and spikes in retries
- CPU and Memory per worker
- Mean time to recover (MTTR) — measured from alert timestamp to first successful batch

## Assumptions
- Each warehouse runs a small set of worker replicas behind a job queue
- No managed SaaS telemetry beyond Sentry; everything is instrumented from code

(See /src and /scripts for the instrumentation examples and exporter code.)
