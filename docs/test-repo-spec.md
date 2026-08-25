# test-repo-spec.md — tokens the corpus relies on

This documents exactly which source / sink / sanitiser tokens the corpus uses, so the
engine can be aligned to it. If the engine's real token lists differ, either update the
engine or update the corpus — they must agree. (This doc was generated to match the
input shapes in the test plan; treat it as the contract, and correct it if the engine
team's lists differ.)

## Sources — PII read from a person-noun receiver

A source is `<person>.<pii_field>` where the receiver resolves to a **person class**
(here `User`, in-repo). A `.name`/`.email` on a non-person (`Product`) is NOT a source
— that is the person-noun gate (X-NAMEGATE, N-NOTPII).

PII fields present on `User`, by harm tier (see Severity):

- severe:   `aadhaar`, `password`
- elevated: `pan`, `income`
- standard: `email`, `phone`, `name`, `address`, `gender`

## Sinks — by symbol, receiver-constrained where noted

| Rule | Control | Sink token | Notes |
|------|---------|-----------|-------|
| pii-in-log | DPDP-002 | `logger.info`, `System.out.println` (Java) | |
| pii-external-api | DPDP-028 | `requests.post` | |
| pii-to-llm | DPDP-028 | `openai.chat.completions.create` | |
| pii-to-third-party | DPDP-028 | `stripe.customers.create`, `razorpay.customer.create` | name recipient; cross-border SUSPECTED only |
| pii-to-file | DPDP-006 | `Path(...).write_text` | |
| pii-in-url | DPDP-004 | `urlencode` | |
| pii-in-cache | DPDP-027 | `cache.set` | receiver must be `cache`, not bare `r` (X-ALIAS) |
| pii-in-email | DPDP-029 | `mailer.send_mail(body=...)` | only `body=` arg; `to=` excluded (N-RECIP) |
| pii-in-storage | DPDP-025 | `localStorage.setItem` (JS) | |
| sqli | DPDP-032 | `cursor.execute` | source is request input, not PII |

## Sanitisers — three layers (any one clears the flow)

1. **verb:** `mask` (name-based).
2. **crypto lib:** `bcrypt.hashpw` (Python), `Cipher.doFinal` (Java).
3. **custom:** any name listed under `custom_sanitisers` in `.svorah.yml` — here `to_stars`.

Plus the **consent gate**: a call to `check_consent(...)` that *dominates* the sink in
the CFG (early-return guard) clears the flow (N-CONSENT).

SQL-specific barrier: `int(...)` cast on the tainted value (N-SQLCAST).

## Cross-border (§16)

See the full rule below — the code agent only ever emits **suspected**, never confirmed.

## Config (`.svorah.yml`)

- `custom_sanitisers: [to_stars]`
- `excluded_paths: ["tests/**"]`

## Severity = PII harm tier (not the rule)

- CRITICAL: aadhaar, biometric, health, bank_account, card_number, password, religion,
  caste, sexual_orientation, political_opinion, criminal_record, child_data
- HIGH: pan, passport, driving_licence, voter_id, national_id, tax_id, upi_id, income,
  auth_token, security_question, location, photograph, date_of_birth, employment, contacts
- MEDIUM: everything else (email, phone, name, address, gender, …)

Decision: `ifsc` is **MEDIUM**. An IFSC code alone is a public bank-branch identifier (not
an account number), so it is not treated as severe. If your harm taxonomy currently maps IFSC
to a bank-identifier → SEVERE tier, that mapping is what to change — the corpus label is MEDIUM
by intent. (FN-INDIANIDS)

## Source matching rules (from the edge-case corpus)

- **Token equality, not substring:** `pan` must not match inside `expand`; `dob` must
  not match inside `dobson`. (FP-TOKENS)
- **Field-name vs value:** `email_regex`, `email_template_id`, `nameField` are names
  *about* PII, not PII values — no source. (FP-TOKENS)
- **Person-noun gate:** a PII field only counts when its receiver is a person
  (`user`), not `product` / `table` / `challenge` / `config` / anonymous `_tmp_56`. (FP-RECEIVER, N-NOTPII, X-NAMEGATE)
- **Naming normalisation:** match camelCase / snake / suffix — `aadhaarNumber`,
  `emailAddress`, `user_phone`. (FN-NAMING)
- **Also sources:** subscript (`user["aadhaar"]`, `body['email']`), values inside a
  dict/list container, and Java getters (`user.getAadhaar()`).

## Non-sink exclusions (must NOT be treated as sinks)

- bare `.write(` (only `Path(...).write_text` is the file sink) — `response.write`, `stream.write`
- reads: `localStorage.getItem`
- `'log'` as a substring of a receiver: `catalog.save`, `dialog.show`, `backlog.add`
- non-DB look-alikes of `execute`: `doc.text`, `res.raw`, `pdf.render`
- template render / DB update: `res.render({...})`, Mongo `{$set: ...}`
- **assignment, not a call:** `openai.api_key = ...`, `stripe.apiKey = ...`
- email `to=` recipient (only `body=` content is a sink) — even with `subject=`

## Taint propagation / sanitiser rules

- **Do NOT launder:** `str(x)`, f-strings, `.strip()` and other representation changes
  keep the taint. (FN-TRANSFORMS)
- **Alias chains** propagate taint; **dedup** to one finding per `file:line`. (FN-ALIAS, ORD-DEDUP)
- **Order matters:** a sanitiser must be on the path *before* the sink; a mask *after*
  the leak does not help. (ORD-BEFOREAFTER)
- **Argument-scoped:** sanitising one argument does not clear another. (FN-PARTIAL)
- **Custom-sanitiser name must match exactly** the `.svorah.yml` entry — `toStars` ≠
  `to_stars` ⇒ still fires. (FN-NAMEMISMATCH)
- **Consent must dominate** the sink (CFG). A check in another branch, or after the
  sink, does not clear it. (N-CONSENT vs FN-NONDOM-CONSENT)

## Cross-border (§16) — the code agent SUSPECTS, it never CONFIRMS

**Principle (applies to §16, encryption-at-rest, and storage location alike):** the code
agent detects data **movement** and **recipients**. It does **not** assert states of
**infrastructure** or **law** (in-India, encrypted-at-rest, lawful). Those verdicts require
the cloud scan, a client declaration, or a human (DPO). Asserting cross-border from the
brand alone is the bug this corpus guards against.

What the code agent may emit — never `confirmed` / `true`:

- `suspected` — recipient is a foreign-HQ vendor (`stripe`, `openai`, `anthropic`) **or** a
  literal foreign region hint is in source (`region_name="us-east-1"`).
- `not_suspected` — recipient is an India-HQ vendor (`razorpay`, `paytm`) **or** a literal
  India region hint (`ap-south-1`, `centralindia`, `asia-south1`).
- `resolved_domestic` — a `.svorah.yml` `data_residency:` declaration resolves the recipient.
- `not_asserted` — unknown recipient, no region hint. Flag the flow + recipient, say nothing
  about residency.

Region-hint literals the code agent should grab when present:
- AWS India: `ap-south-1`, `ap-south-2` · Azure India: `centralindia`, `southindia`,
  `westindia` · GCP India: `asia-south1`, `asia-south2` · anything else = foreign hint.

The verdict is upgraded elsewhere: **cloud scan** reads the real region and turns `suspected`
→ confirmed §16 or clears it; **DPO/RoPA** attests processor location for SaaS where it is a
contract choice. (X-XBORDER, X-REGION-HINT)
