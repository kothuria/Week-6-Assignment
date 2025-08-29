#!/usr/bin/env python3
"""Prometheus metrics exporter demo (uses psutil)"""
from prometheus_client import start_http_server, Histogram, Counter, Gauge
import psutil, time, random, threading

BATCH_LATENCY = Histogram('inventory_batch_seconds', 'Inventory batch latency seconds', buckets=(0.01,0.05,0.1,0.2,0.5,1,2,5))
BATCH_SUCCESS = Counter('inventory_batch_success_total', 'Total successful batches')
BATCH_FAILURE = Counter('inventory_batch_failures_total', 'Total failed batches', ['error'])
ITEMS_PROCESSED = Counter('inventory_processed_items_total', 'Total items processed')
CPU_GAUGE = Gauge('system_cpu_percent', 'System CPU percent')
MEM_GAUGE = Gauge('system_memory_percent', 'System memory percent')
WORKERS = Gauge('worker_active_replicas', 'Active worker replicas')

def sample_system_metrics():
    while True:
        CPU_GAUGE.set(psutil.cpu_percent(interval=1))
        MEM_GAUGE.set(psutil.virtual_memory().percent)
        time.sleep(2)

def simulate_activity():
    while True:
        with BATCH_LATENCY.time():
            # synthetic work
            time.sleep(random.uniform(0.02, 0.2))
        if random.random() < 0.995:
            BATCH_SUCCESS.inc()
            ITEMS_PROCESSED.inc(random.randint(1,100))
        else:
            BATCH_FAILURE.labels(error='E_TIMEOUT').inc()
        WORKERS.set(random.randint(1,6))
        time.sleep(0.1)

if __name__ == '__main__':
    start_http_server(9100)
    import threading
    threading.Thread(target=sample_system_metrics, daemon=True).start()
    threading.Thread(target=simulate_activity, daemon=True).start()
    print('Metrics exporter running on :9100')
    while True:
        time.sleep(60)
