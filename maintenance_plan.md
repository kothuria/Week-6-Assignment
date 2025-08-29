# Maintenance Plan (step-by-step)

## Patch & Release
1. Feature branch → PR → CI runs unit tests and linters
2. Use semantic versioning. When ready, create a release PR that bumps `version` and adds CHANGELOG entry.
3. GitHub Actions builds the Docker image; tag release `vX.Y.Z` and push to Registry.

## Dependency Management
- Maintain `requirements.in` and use `pip-compile` (pip-tools) to create locked `requirements.txt`.
- Enable Dependabot for dependency and security PRs.
- Routine: `monthly` dependency bump window; immediate patch for critical CVEs.

## Scaling Strategy
- 5×: scale replicas and tune worker concurrency (process-level horizontal scale)
- 10×: add job sharding by warehouse, partition the queue, increase monitoring cardinality carefully
- 100×: introduce autoscaling (Kubernetes HPA), add rate-limiting, use regional clusters and sharded Prometheus remote_write to long-term TSDB

## Recovery Plans (code-level)
- Idempotent processing and at-least-once semantics with visibility timeouts
- Retries with exponential backoff; after N retries send item to dead-letter queue
- Use health checks to trigger orchestrator restart for stuck workers

## Hotfix process
- Create `hotfix/*` branch off `main`, small patch with highest test coverage, CI runs, create tag like `v1.2.3-hotfix.1`, deploy only to affected region
