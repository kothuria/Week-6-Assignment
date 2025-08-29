#!/usr/bin/env python3
"""Generate synthetic inventory bot logs (JSON lines).

Usage:
    python scripts/generate_fake_logs.py --count 10000 --out data/fake_logs.jsonl
"""
import argparse, random, json, os, time, uuid, datetime
from faker import Faker
fake = Faker()

def mk_event(i):
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    duration_ms = max(1, int(random.gauss(200, 100)))
    status = random.choices(['success','failure','retry'], weights=[0.985,0.01,0.005])[0]
    err = None
    if status != 'success':
        err = random.choice(['E_TIMEOUT','E_DB','E_UNIQUE_CONSTRAINT','E_NETWORK'])
    event = {
        'timestamp': ts,
        'req_id': str(uuid.uuid4()),
        'batch_id': f'batch-{i%5000}',
        'duration_ms': duration_ms,
        'status': status,
        'error_code': err,
        'warehouse_id': f'wh-{random.randint(1,50)}',
        'items': random.randint(1,100),
        'message': fake.sentence(nb_words=8)
    }
    return event

def main(count, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as fh:
        for i in range(count):
            fh.write(json.dumps(mk_event(i)) + '\n')
    print(f'Wrote {count} events to {out}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=10000)
    parser.add_argument('--out', type=str, default='data/fake_logs.jsonl')
    args = parser.parse_args()
    main(args.count, args.out)
