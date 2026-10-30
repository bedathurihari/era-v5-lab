# Medicine sheet: ind-te-fw2 (bedathurihari)

**Status: 500/500 text fields scanned, but manual document-by-document reading and adjudication are still pending.** All 500 rows are marked `partial` and all counts below are provisional candidates.

**Harm testing: NOT RUN.** The official Telugu gold set owned by Data A/B was not available. A medicine cannot be claimed to pass the <=1% threshold without that set.

## Candidate inventory

| Code | Candidate documents | Official gold test |
|---|---:|---|
| B2 | 4 | Not run |
| C1 | 32 | Not run |
| C2 | 9 | Not run |
| D1 | 2 | Not run |
| D3 | 18 | Not run |
| F1 | 12 | Not run |
| F3 | 1 | Not run |
| H2 | 4 | Not run |

## Medicine proposals — candidate codes appearing more than five times

### C1 — Related links and boilerplate (32 candidate documents)

1. **Examples requiring human confirmation:**
- `ab4df107c4d439c6`: C1 candidate; see exact positional evidence in `labels.csv`
- `93e12eda26737171`: C1 candidate; see exact positional evidence in `labels.csv`
- `142ddb551bbdbbd2`: C1 candidate; see exact positional evidence in `labels.csv`

2. **Medicine:** Remove only verified isolated cross-link lines; preserve article text.

```python
import re
RELATED = re.compile(r"(?im)^\s*(?:Also Read|Read More|ఇది కూడా చదవండి|ఇదీ చదవండి)\s*[:：-]\s*[^\n]*$")
def fix_c1(text):
    return RELATED.sub("", text)
```

3. **Action and side effects:** Fix verified navigation line. Side effects: meaningful related citations may be deleted.

4. **Gold-set harm test:** NOT RUN (gold set unavailable). Gold documents changed = unmeasured; dropped = unmeasured; unique affected = unmeasured; result = UNKNOWN. Reject if affected / total gold documents > 0.01.

5. **Required next step:** inspect the three examples in full, run on Data A/B's Telugu clean gold set, count changed and dropped documents, and inspect any false positives.

### C2 — Repeated whole lines (9 candidate documents)

1. **Examples requiring human confirmation:**
- `6faa50209f00b4cf`: C2 candidate; see exact positional evidence in `labels.csv`
- `701668a26b4c5508`: C2 candidate; see exact positional evidence in `labels.csv`
- `f3afb012f3c52eb2`: C2 candidate; see exact positional evidence in `labels.csv`

2. **Medicine:** Only remove a repeated line after human verification it is redundant scaffolding.

```python
def fix_c2(text, verified_lines):
    seen=set();out=[]
    for line in text.splitlines(keepends=True):
        key=line.strip()
        if key in verified_lines:
            if key in seen: continue
            seen.add(key)
        out.append(line)
    return "".join(out)
```

3. **Action and side effects:** Fix only approved boilerplate repetitions. Side effects: legitimate repetition in tables and structured prose.

4. **Gold-set harm test:** NOT RUN (gold set unavailable). Gold documents changed = unmeasured; dropped = unmeasured; unique affected = unmeasured; result = UNKNOWN. Reject if affected / total gold documents > 0.01.

5. **Required next step:** inspect the three examples in full, run on Data A/B's Telugu clean gold set, count changed and dropped documents, and inspect any false positives.

### F1 — Potential personal information (12 candidate documents)

1. **Examples requiring human confirmation:**
- `c5a74a6de69221b8`: F1 candidate; see exact positional evidence in `labels.csv`
- `b6ddb1f2f2e4456f`: F1 candidate; see exact positional evidence in `labels.csv`
- `4c9db4e00856fe76`: F1 candidate; see exact positional evidence in `labels.csv`

2. **Medicine:** Detect contact offsets and have a reviewer confirm whether they identify a private person before redaction.

```python
import re
EMAIL=re.compile(r"(?<![\w@])[A-Za-z0-9][A-Za-z0-9._%+\-]{0,64}@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}(?![\w@])")
PHONE=re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")
def find_offsets(t):
    return [("email",m.start()) for m in EMAIL.finditer(t)] + [("phone",m.start()) for m in PHONE.finditer(t)]
# Never copy the actual values into public files.
```

3. **Action and side effects:** Redact confirmed private values only. Side effects: public contact numbers may be incorrectly flagged.

4. **Gold-set harm test:** NOT RUN (gold set unavailable). Gold documents changed = unmeasured; dropped = unmeasured; unique affected = unmeasured; result = UNKNOWN. Reject if affected / total gold documents > 0.01.

5. **Required next step:** inspect the three examples in full, run on Data A/B's Telugu clean gold set, count changed and dropped documents, and inspect any false positives.

### D3 — Mixed Telugu and English (18 candidate documents)

1. **Examples requiring human confirmation:**
- `fdb1b904679948c6`: D3 candidate; see exact positional evidence in `labels.csv`
- `da88f8127113b503`: D3 candidate; see exact positional evidence in `labels.csv`
- `c7c7cd3b65e5823a`: D3 candidate; see exact positional evidence in `labels.csv`

2. **Medicine:** Natural code switching is valid; do not delete or force English-only cleanup.

```python
def fix_d3(text):
    return text # intentionally preserves valid Telugu/English mixtures
```

3. **Action and side effects:** Preserve / defer. Side effects: a no-op does not repair actual translation failures.

4. **Gold-set harm test:** NOT RUN (gold set unavailable). Gold documents changed = unmeasured; dropped = unmeasured; unique affected = unmeasured; result = UNKNOWN. Reject if affected / total gold documents > 0.01.

5. **Required next step:** inspect the three examples in full, run on Data A/B's Telugu clean gold set, count changed and dropped documents, and inspect any false positives.

## Gold-set harm test driver

```python
def harm_test(gold_texts, cleaner):
    if not gold_texts: raise ValueError('Official gold set required')
    changed=dropped=0
    for text in gold_texts:
        new=cleaner(text)
        changed += int(new is not None and new != text)
        dropped += int(new is None)
    affected=changed+dropped
    return {'N':len(gold_texts),'changed':changed,'dropped':dropped,
            'affected':affected,'rate':affected/len(gold_texts),
            'pass':affected/len(gold_texts)<=0.01}
```

## Incomplete work
- Read every document fully and correct the partial labels; do not relabel automatically as full.
- Finalize confirmed disease frequencies and three authentic examples per qualifying code.
- Obtain the Telugu gold set and run each medicine; no invented harm-test result.
- Update the existing diagnosis PR #58, not a new PR. Do not commit the Parquet, personal data or secrets.
