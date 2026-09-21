# Efficient application autofill

Read the confirmed profile once and inventory the current form by section. Map every field to a sourced fact, context-specific draft, or unresolved question. Reuse confirmed facts; do not ask again for known information. Batch stable independent field operations sequentially in a supported browser call, then review the section.

- Replace text with `fill` or select-all-and-type; never append a second entry to verify the first.
- Missing/redacted accessibility values are unknown, not empty. Inspect the rendered email/phone before re-entry.
- Preserve correct user edits. Match existing education/work groups by institution/employer, degree/title and dates before adding another.
- Refresh UI after structural changes. Click observed dropdown options; never press Enter while loading or blindly inside forms.
- Cache references to confirmed facts, not secrets. Reuse prose only when question, employer, role, time window and source revision match; otherwise compose a grounded answer for the new context.
- Authorization answers are country- and wording-specific. Never infer unknown answers, sensitive traits, residency, or qualifications.
- Attach the verified role-specific resume; confirm its visible filename and check whether parsing changed any form fields.
- Review required fields and current permission before the separately authorized submit step. One click, then receipt verification; ambiguous outcomes are not Applied.

The generic Codex skill `job-application-autofill` provides additional mappings and ATS recipes when installed. This reference remains usable without it. Browser host rules and the kit's permissions/review checks continue to apply.
