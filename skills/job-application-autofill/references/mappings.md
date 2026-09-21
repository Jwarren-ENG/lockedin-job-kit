# Field mapping rules

| Form intent | Source and checks |
| --- | --- |
| Email / phone / name / links | Exact confirmed profile field; replacement only. Honor country prefix separately. |
| Current location | Current address/location, not permanent home. Select an observed truthful geographic option. |
| Permanent residence / legal residency | Use the explicit applicable fact. An ID or school address alone does not establish residency. |
| Education | All requested degrees, including completed undergraduate and current graduate education; match existing groups before adding. Use confirmed dates and truthful available discipline options. |
| Employment | Confirmed employer/title/dates; current employment checkbox must agree with end date. Previous employment question is employer-specific. |
| Work authorization | Match country, now versus future, sponsorship versus authorization, and exact positive/negative wording. Never use one global yes/no. |
| Graduation / availability | Degree date differs from work availability. Do not infer full-time availability from graduation or internship interest. |
| Experience years / tools | Supported experience only; do not count overlapping roles twice or treat familiarity as mastery. |
| Salary | Confirmed target, currency, period, base versus total. No inferred minimum. |
| Demographics | Exact saved voluntary preference and current form options; keep race and ethnicity distinct; never infer. |
| Consent | Match exact purpose to existing permission; broad consent is not a factual attestation. |
| Company interest / project / AI use | Current employer and role context plus confirmed experience. Respect excluded topics and employer assistance rules. |

Private cache entry shape (reference-based, not personal sample data):

```json
{
  "question_exact": "<full observed question>",
  "semantic_key": "<profile concept>",
  "source_ref": "<private file and field>",
  "source_revision": "<revision or timestamp>",
  "context": {"company": null, "role": null, "country": null, "time_window": null},
  "kind": "fact-reference",
  "last_verified": null
}
```

Normalize whitespace only for lookup. Do not remove negation or meaningful punctuation/qualifiers. For ambiguous matches, inspect rather than use a fuzzy-match score as evidence. Contextual answers require context matching even with identical wording. Historical submission does not make an answer permanently current.

Regression review scenarios:
1. Email omitted in AX after entry -> inspect screenshot; never append.
2. Undergrad already entered by user -> keep; do not add duplicate school.
3. US authorization followed by Canadian authorization -> separate fact; unknown Canadian answer stays unresolved.
4. Same "Why this company?" at another employer -> new grounded answer.
5. Dropdown loading -> wait for observed choices; no Enter.
6. Resume parse overwrites current title -> restore confirmed correction and recheck.
7. Submit result interrupted -> Submission uncertain; no second click.
