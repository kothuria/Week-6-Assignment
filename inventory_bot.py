#!/usr/bin/env python3
"""Simple inventory bot worker (demo mode) with instrumentation and structured logging"""
import os
import json
import time
import random
import argparse
import logging
import logging.handlers
from prometheus_client import Histogram, Counter, start_http_server
import sentry_sdk

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Metrics
REQUEST_LAT = Histogram('inv_batch_seconds', 'Inventory batch duration seconds')
BATCH_OK = Counter('inv_batch_ok_total', 'Successful inventory batches')
BATCH_ERR = Counter('inv_batch_err_total', 'Errored inventory batches', ['err'])

# Logging config: write JSON lines to logs/inventory.log
handler = logging.handlers.TimedRotatingFileHandler(
    'logs/inventory.log', when='midnight', backupCount=7
)
formatter = logging.Formatter(
    json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s"
    })
)
handler.setFormatter(formatter)

logger = logging.getLogger('inventory')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Optional Sentry init (set SENTRY_DSN env var to enable)
dsn = os.environ.get('SENTRY_DSN')
if dsn:
    sentry_sdk.init(dsn, traces_sample_rate=0.0)
    logger.info('Sentry initialized')

def process_batch(batch_id):
    """Process a single inventory batch."""
    with REQUEST_LAT.time():
        start = time.time()
        # synthetic processing
        time.sleep(max(0.01, random.gauss(0.05, 0.03)))
        if random.random() < 0.99:
            BATCH_OK.inc()
            logger.info(json.dumps({
                'batch_id': batch_id,
                'status': 'success',
                'duration_ms': int((time.time() - start) * 1000)
            }))
            return True
        else:
            err = 'E_TIMEOUT'
            BATCH_ERR.labels(err).inc()
            logger.error(json.dumps({
                'batch_id': batch_id,
                'status': 'failure',
                'error': err
            }))
            if dsn:
                sentry_sdk.capture_message(f'Batch failure {batch_id}: {err}')
            return False

def main(demo):
    """Main loop to process batches."""
    start_http_server(9101)
    i = 0
    while True:
        batch_id = f'batch-{i % 1000}'
        process_batch(batch_id)
        i += 1
        if demo and i > 5000:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    args = parser.parse_args()
    main(args.demo)
