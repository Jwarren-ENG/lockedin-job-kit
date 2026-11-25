# Release checks

## Version 0.4.0

The guided setup runs offline. The Chrome test uses a fictional résumé and verifies extraction, edits, the confirmation step, prefilled fields, named chat permission, excerpt-only use, back navigation, the private download and reset. The mobile layout was checked at 390 pixels. No web request or JavaScript error occurred during the test.

Run `python3 -m unittest discover -s tests`, `python3 -m unittest discover -s skills/job-application-autofill/scripts`, `BROWSER_CHANNEL=chrome node tests/test-setup.mjs` and `node tests/test-workbook.mjs`. The suites check opt-in defaults and revocation, legacy profiles and pause state, local midnight, empty initial source lists, spreadsheet preservation, archive contents, offline guide links and release checksums.

A local Ollama session with qwen2.5:7b asked for the résumé, extracted the stated details from a fictional example and presented the optional history choices after confirmation. It also repeated the confirmation. The prompt guides a model; applicants should review its output. Hosted subscription limits and a new user's scheduling or conversation permissions depend on that account and require a setup check.

## v0.3.0 validation

Executed: 23 tracking/Obsidian tests and 28 autofill regression tests, release allowlist audit, package generation and diff whitespace checks. Autofill tests cover duplicate contact prevention, scoped aliases, stale sources, disclosure gates and evidence-grounded answers. Run `python3 -m unittest discover -s skills/job-application-autofill/scripts -p 'test_*.py' -v` in addition to the main suite.

The external Codex manifest validator could not run in this environment because PyYAML is unavailable. Both JSON manifests parse and only their version changed. No UI or workbook implementation changed; earlier UI checks were not rerun. Live employer submission and cross-host installation remain unverified.

# Validation for v0.1.0

## v0.2.0 additions

The Python suite now includes optional Obsidian export checks: preserve personal note sections, keep rejected applications in historical submission counts, reject ambiguous interview timestamps, update rescheduled events without duplicates, and remove cancelled interviews from upcoming views. Run the suite and release audit on every change; All tests use fictional data only. GitHub Actions is not configured; run these checks locally.

The original v0.1.0 checks below describe the initial development environment, not universal host certification. Phone push delivery, personal sync accounts and another person's end-to-end application flow still require their own tests.

Executed locally using fictional applicants and temporary workspaces:

- 20 Python workflow tests: initialization and no-overwrite, permission defaults and scoped updates, consent and unknown-field blocking, pause/revocation, resume hash changes, stale review rejection, duplicate roles/URLs, reservation and daily limits, evidence requirement, email event deduplication, status history, CSV formula escaping and exclusion of profile fields.
- Browser setup smoke test in headless Chrome: unchecked defaults, required storage consent, separate demographic storage consent, private JSON download, form reset, zero HTTP requests and zero JavaScript errors. Full-page layout inspected.
- Spreadsheet helper smoke test using the available artifact runtime: initial creation, append, status refresh, preserved user Notes and unrelated worksheet, formula-looking text not executed. Rendered output inspected.
- Codex plugin manifest validator, Claude plugin validator and all five skill frontmatter validators passed.

Run Python tests with `python3 -m unittest discover -s tests -v`. JavaScript tests require the host's Playwright/artifact runtime; use `BROWSER_CHANNEL=chrome node tests/test-setup.mjs` where Chrome is installed and `node tests/test-workbook.mjs`. These are optional development dependencies, not hidden installs.

Not verified end-to-end: installation and execution in a separate person's Codex/Cowork account; live employer submissions; their password manager; native scheduling across every host; Google Sheets connector; all ATS variations. No live application, account or scheduler was created by these tests. PDF fixture in gate tests checks hashing only, not PDF rendering; real resumes must be compiled and visually verified during use.

The permission gate is a local workflow check, not a security sandbox for arbitrary model/tool actions. The host assistant must enforce its skill instructions and platform controls. A checked field or synthetic test does not prove an employer received an application.
