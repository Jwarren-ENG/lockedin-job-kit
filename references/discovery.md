# Discovery and fit

Start with the person's targets and constraints. The active list lives in the private workspace's sources.json. Fresh workspaces start empty. On first search, read any sources already chosen or supplied, find a small set of direct employers and specialist or regional sources for this search, and inspect a sample posting before adding a source. Save each source's name, URL, role or cohort coverage, geography, reason and date actually checked. Keep existing reviewed sources across upgrades. Revisit poor sources when the search changes.

The bundled assets/sources.json is an example catalog. For associate product roles, try [APM List](https://apmlist.com/) and the relevant product cohort. For new graduate software, quantitative finance or product, inspect the appropriate current category of [SimplifyJobs](https://github.com/SimplifyJobs/New-Grad-Positions). For finance, healthcare, trades and other paths, find employers hiring in the person's area and a relevant professional association or specialty board. Use local terminology, licenses and country-specific sources. Follow a lead to a live role on the employer site. A list name, last update or employer headquarters does not establish eligibility, posting date or work location.

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
