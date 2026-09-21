# Discovery and fit

Use the person's configured criteria, never hardcoded NYC/US/PM defaults. Seed source: https://apmlist.com/ for APM searches, then verify on the official posting. Save other relevant resources in sources.json with location, role coverage and last successful check. Respect source access controls.

Also use https://github.com/jobright-ai/2026-Product-Management-New-Grad when relevant. The repository year does not establish eligibility; verify each actual graduation cohort and start date. It includes unrelated titles and locations, so apply the user's filters. `assets/sources.json` seeds both sources into each new private workspace.

For each job preserve employer, title, official URL, requisition, exact location/work mode, seniority, eligibility/timing, published compensation basis, deadline/time zone if known, employer posting date if stated, first-seen time, fit reasons, gaps and next action. Save a source excerpt or reference for material claims. A headquarters location is not the job location. A job title does not establish new-grad eligibility. Internships can require enrollment after the term; compare actual graduation and start dates. Work authorization and clearance eligibility are separate.

Use salary_min/max as numbers or null, currency and pay_period separately. Do not mix base with equity/bonus or assume annual versus hourly. A high-pay preference is not a salary guarantee. Unknown mandatory criteria keep the role in review, not automatic submission.

Job JSON for add-job:
```json
{"company":"Example Employer","role":"Operations Analyst","url":"https://example.com/careers/operations-analyst","requisition":"EX-101","location":"User-selected location","salary_min":null,"salary_max":null,"currency":"USD","pay_period":"year","posted_at":null,"next_action":"Verify eligibility","notes":"Fictional example only","skills_to_learn":["SQL joins"]}
```

Reserve exact requisitions even if the URL changes. Company aliases and external ATS redirects require manual reconciliation. Do not submit simultaneous applications to the same role under alternate titles. Application databases are private and must never be included in the shareable plugin.

## Freshness and rotation

Use https://github.com/jobright-ai/2026-Product-Management-New-Grad as an optional PM lead source. Its repository name and aggregator date do not prove cohort eligibility or employer posting date. Exclude retail product demonstration from PM results.

A JavaScript shell, empty text extraction, or dynamic empty-state template is an access limitation, not a closed role. Inspect the live page with supported browser tools before declaring it unavailable. A redirect to a generic board is not the original job description. Preserve prior status if current verification fails.

Record actual coverage (filters, pages or excerpt boundaries), attempted_at, last_successful_check, and next employer rotation. Persist watch and excluded decisions by employer/requisition with reasons. Do not repeatedly investigate unchanged unavailable roles or alert on unchanged blockers. A low compensation range is a ranking factor, not an invented user salary floor. Prepare strong authorized matches before ending the run; use watch status only for a concrete unresolved fit question.
