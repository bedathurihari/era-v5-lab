"""Compare only deterministic training metrics; performance timers naturally vary."""
import json,sys
if len(sys.argv)!=3:raise SystemExit('Usage: compare_runs.py run1.jsonl run2.jsonl')
def stable(p):
    return [{k:r[k] for k in ['step','loss_ntp','loss','lr']} for r in map(json.loads,open(p))]
a,b=map(stable,sys.argv[1:]);assert len(a)==len(b) and a==b,'NONREPRODUCIBLE: loss metrics differ'
assert a[-1]['loss']<a[0]['loss'],'LOSS DID NOT FALL'
print('PASS: same seed, equal per-step loss, decreasing final loss')
