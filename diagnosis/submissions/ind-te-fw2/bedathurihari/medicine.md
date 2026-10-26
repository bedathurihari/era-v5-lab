# Medicine sheet: ind-te-fw2 (bedathurihari)

> WORK IN PROGRESS — do not treat these as final confirmed diagnoses or verified harm tests.
> Source: automated whole-text scan of first 150 / 500 documents on 26 Oct 2026.
> Manual full-document review, remaining 350 documents and Telugu gold-set testing are pending.

## Preliminary disease counts (first 150 rows only)

| Candidate | Documents | Status |
|---|---:|---|
| F1 potential personal information | 5 | Human adjudication pending; never reveal values |
| B2 HTML tags | 2 | Human adjudication pending |
| C1 footer/boilerplate | 1 | Human adjudication pending |
| C2 repeated lines | 1 | Human adjudication pending |

The DISEASES.md rule requires a medicine **for each confirmed disease appearing more than five times** in the full pack. None of the above candidate types exceeds five in the first 150. These preliminary counts do not predict the full 500-document counts.

## Pending medicine and harm-test protocol

1. Complete manual adjudication and full document coverage.
2. Count confirmed disease occurrences and gather three exact examples per disease; for F1/E3, only list type and offset, never the value.
3. Propose a narrowly scoped cleaner with Python/regex and a fix/drop policy.
4. Test it against the Telugu gold set controlled by Data A/Data B. Record gold set size N, documents changed C, documents dropped D, and affected union U.
5. Reject the medicine if U/N > 0.01 (more than 1%). Report false positives and any damage to valid Indic ZWJ/ZWNJ, vowel signs, nukta and normal forms.
6. Never claim harm-test pass before the gold set has been supplied and run.

**Harm-test status:** NOT RUN (gold dataset not provided). No invented pass percentages.
