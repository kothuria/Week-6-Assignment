#!/usr/bin/env python3
"""Retry with exponential backoff and dead-letter example"""
import time, functools, logging

logger = logging.getLogger('recovery')

def retry(max_retries=3, base_backoff=0.5, backoff_factor=2):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logger.warning(f'Attempt {attempt} failed: {e}')
                    if attempt > max_retries:
                        logger.error('Max retries exceeded; sending to dead-letter')
                        # send to DLQ logic here (placeholder)
                        raise
                    sleep = base_backoff * (backoff_factor ** (attempt-1))
                    time.sleep(sleep)
        return wrapper
    return deco
