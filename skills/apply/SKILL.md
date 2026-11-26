---
name: apply
description: Tailor a verified LaTeX resume and prepare or submit a specific job application under the user's Job Search Kit permissions.
---

# Apply to a role

When the user starts this task from Project Pluto, the handoff includes their private tracker and desktop workspace. Read the supplied desktop database in SQLite read-only mode. Match its jobs, immutable submissions and events against the kit tracker before retrying a role. An unresolved difference is a reason to check the employer receipt. Write verified outcomes using the usual kit commands and refresh the connected dashboard.


Read [permissions](../../references/permissions.md), [resume workflow](../../references/resumes.md) and [tracking](../../references/tracking.md). The scripts validate records but do not control browser tools; you must enforce the same rules on every tool action.

1. Verify the official job and its fit against confirmed profile criteria. Confirm ambiguous location, salary, cohort, hours, travel or authorization requirements instead of marking matches_search/eligibility_verified true without evidence. Check the database and relevant receipts for duplicates.
2. Save the official posting and its URL. Tailor only confirmed facts from the authoritative LaTeX and experience bank. Save Company - Role.tex and Company - Role.pdf in the job's folder, sanitize filenames, and use a non-overwriting version when needed. Compile with the host PDF skill, inspect page count and render every page. If no safe LaTeX runtime exists, leave a draft and explain the dependency.
3. Before typing personal data or uploading anything, check use_computer, the approved site and current scope. An address disclosure, including an address embedded in the résumé, requires share_address plus the confirmed address type and recipient scope. If missing, draft privately or omit the address when permitted. Include share_address in consents_needed for any address actually shared. Recheck after permission changes. Use only supported browser controls. Use the chosen application email. Account creation requires its separate permission; generate a unique password in the user's password manager when supported, otherwise hand off. Never copy passwords, MFA codes, session cookies or tokens into files. Do not use a reusable shared password.
4. Fill confirmed answers and record their sources. Read each disclosure and map it to an exact saved category. Never map unknown to No. Optional demographics require both saved exact answers and disclosure permission. Do not infer residency, citizenship, protected traits, former employment or certification eligibility from names, IDs or unrelated answers.
5. Prepare `applications/<id>/review.json` from [review template](../../assets/review-template.json). All booleans need current evidence. Include the role ID, current permission revision, exact resume SHA-256, answer evidence, unresolved questions and required consent categories. Log the terms text/URL and the chosen response. For manual mode, show a concrete application summary and obtain this application's approval; record it in user_submit_approval. Stored preferences never override host confirmation or policy requirements.
6. Immediately before submission, run `reserve <id> <review-file>`. Stop on allowed:false or any command failure. Reload permissions and recheck the live form; if the user revoked authorization, do not submit and record the cancelled attempt as Submission uncertain with a note that no click occurred until reviewed. Perform at most one submit action. Do not complete a prohibited action through another tool.
7. Record a verified portal receipt with status Submitted, preserving timestamp and source. If the response is ambiguous or interrupted, mark Submission uncertain, retain evidence and investigate before any retry. User-confirmed submission is acceptable evidence but label it as such. Update tracker through status/export; do not edit a historical submitted PDF.

An employer assessment is separate from an application. Do not complete a live assessment on the candidate's behalf contrary to its rules. Offer preparation and permitted assistance instead.

For efficient section-level filling, use [the bundled autofill skill](../job-application-autofill/SKILL.md). Its local planner proposes actions; host controls, permission checks and submission evidence still apply.
