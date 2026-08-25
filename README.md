# svorah-test-repo — taint-engine acceptance corpus

> ⚠️ **Intentionally non-compliant test corpus.** Every flow here is a deliberate,
> minimal DPDP violation (or a matched suppression) authored to grade SVORAH's
> taint engine. All data is fake. Do not deploy or reuse this code.

This is the controlled, gradeable corpus behind the SVORAH Taint-Engine Test Plan.
Each rule ships as a **pair**: a positive that must fire and a matched negative that
must be suppressed — plus cross-checks that prove the *model* (severity, cross-border,
receiver/source gating, config layers), not just the plumbing.

## What's here (coverage bar)

- **11 positives** (must fire) — `app/positives/*` + `app/js/p_store.js` + `app/java/.../PLog.java`
- **8 negative mechanisms** (must be suppressed) — `app/negatives/*` + `tests/n_excluded.py` + `app/java/.../NCrypto.java`
- **5 cross-checks** — `app/crosschecks/*` (X-L3TOGGLE re-runs `n_custom.py` with config removed)

Languages: Python (majority), JavaScript (P-STORE), Java (P-JAVA / N-CRYPTO). No Go.

### Edge-case matrix (the hard part)

- **FN-resistance** (`app/fn/*`) — real violations it must still catch: 3-file
  interprocedural flow; non-laundering transforms (`str()`, f-string, `.strip()`);
  camelCase/snake naming; subscript & container sources; alias chains; getter-chain
  loggers; Indian-ID moat (UPI/IFSC/voter-id/PAN); non-dominating consent; partial
  sanitisation; custom-sanitiser name mismatch.
- **FP-resistance** (`app/fp/*`) — look-alikes that must stay silent: non-person/temp
  receivers; token-substring & field-name traps; `log`-substring receivers; non-DB
  `execute` look-alikes; bare `.write`; reads; compound-expr & config-assignment traps;
  recipient-only email.
- **Ordering** (`app/ordering/*`) — sanitiser-before vs -after; two sinks on one line
  (two findings); dedup to one finding per `file:line`; positive+negative in one function.
- **Cross-border, done right** (`app/crosschecks/x_xborder.py`, `x_region_hint.py`) — the
  code agent names the recipient and labels cross-border **suspected**, never confirmed;
  grabs a literal region hint (`us-east-1` vs `ap-south-1`) when present; a `.svorah.yml`
  `data_residency` declaration resolves it. The §16 verdict is deferred to the cloud scan / DPO.

## The answer key

- **[`expected.yaml`](expected.yaml)** — machine-readable; the runner diffs scanner output against it (every finding pinned to `file:line`, control, severity).
- **[`docs/test-repo-spec.md`](docs/test-repo-spec.md)** — the exact source / sink / sanitiser / vendor tokens the corpus uses. **Align the engine to this** (or fix the corpus if the engine's lists differ).

## Layout

```
.svorah.yml                 custom_sanitisers:[to_stars], excluded_paths:["tests/**"]
app/models/user.py          person entity (PII sources)
app/models/product.py       non-person entity (person-noun gate)
app/lib/                    in-repo sanitisers, consent gate, sink objects
app/positives/             P-* cases (one per rule)
app/negatives/             N-* suppressions
app/crosschecks/           X-* model proofs
app/js/                    P-STORE (+ in-repo user model)
app/java/com/svorah/testrepo/  P-JAVA, N-CRYPTO (+ in-repo User)
tests/n_excluded.py         N-EXCLUDED (real flow under an excluded path)
```

Every PII source class is defined **in-repo** so Joern can resolve the cross-file flows
(mandatory for the Java case).

## Scoring targets

| Metric | Target |
|---|---|
| Recall (positives that fire) | ≥ 95% |
| Precision (on this corpus) | 100% |
| False positives (from negatives / excluded paths) | 0 |

## How it's run

```bash
# SVORAH backend, Joern installed:
python -m tests.recall_benchmark --repo /path/to/svorah-test-repo
```

Diff the output against `expected.yaml`. The run passes when every P-/X- case fires as
specified and every N- case (and everything under `tests/**`) yields nothing.

For X-L3TOGGLE: remove `to_stars` from `.svorah.yml` `custom_sanitisers`, re-run, and
confirm `app/negatives/n_custom.py:11` flips from 0 findings to one HIGH (pan, DPDP-006).
