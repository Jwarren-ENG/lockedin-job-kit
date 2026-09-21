---
name: job-application-autofill
description: Fill job applications efficiently from a confirmed profile, with section-level planning, reusable question mappings, tailored attachments, and duplicate-entry prevention. Use for Greenhouse, Ashby, Workday, and other application forms, including resuming partially completed applications.
---

# Job application autofill

Use the user's current authorization and the host's supported browser controls. This skill does not expand permissions. Prefer the user's chosen browser; in Codex use the internal browser unless the user chooses otherwise. Never inject DOM mutations, call hidden submission endpoints, or bypass security controls.

## Load once, then fill by section

Default to a single-link workflow: deduplicate the role, prepare/reuse its current truthful resume, fill routine fields in batches, draft all permitted unique answers together, then perform one final review. Do not ask for known facts or routine reversible steps. Collect genuinely missing facts into one concise request after completing independent work. Keep host-required action-time confirmations at the actual boundary.

Within the same run, reuse loaded profile and experience context while sources are unchanged. Reopen only files changed by the user or task. Do not reread entire history for routine fields. Reuse an existing role-specific PDF only when its role, source facts and current requirements still match; preserve historical submitted copies.

For recurring application work, use the executable [planner workflow](references/planner.md). Exact confirmed question mappings are resolved by `scripts/autofill.py`; only unmatched written questions go to contextual drafting. The helper emits a plan for the supported browser tool, not browser automation or submissions.

1. Read the project's confirmed profile, experience bank, demographic preferences where authorized, resume source, application record, and current user corrections. Resolve conflicts in favor of current explicit corrections; never infer missing personal facts. Deduplicate employer + requisition before applying.
2. Inspect the live application. Inventory each visible section in one pass: exact question, control type, required state, available options, current value visibility, and repeat-group identity. Read the full question, including negation and country. A resume parse is provisional, not a source of truth.
3. Plan a section before entering it. Assign each field a source and action: **keep**, **replace**, **select**, **attach**, **inspect**, or **unresolved**. Use [mapping rules](references/mappings.md). Reuse confirmed facts without asking again. Handle known independent fields sequentially within one tool call when supported; do not run concurrent mutations on the same form.
4. Fill standard fields first, then education/work groups, authorization, role questions, disclosures, and attachments. Refresh the UI after dropdown loads, adding/removing a group, navigation, or other structural change. Use fresh semantic locators rather than stale numeric indices.
5. Review once per stable section rather than after every keystroke. Revisit only changed, unresolved, or invalid fields. After final navigation perform a full review including uploaded filename and validation errors.

## Never append duplicate values

- Use a supported replacement operation such as `fill` for text. If only keyboard input exists, focus and select the entire field before typing.
- An omitted/redacted AX or DOM value is **unknown**, not empty. Inspect the rendered field before re-entry. A screenshot is particularly useful for email and phone.
- Keep correct user-entered answers. If a correction is necessary, replace once and verify once. Never type again merely because a snapshot omitted the value.
- Education/work groups are keyed by institution/employer + degree/title + dates. Match existing groups before adding; preserve completed undergraduate and current graduate entries separately.
- Never press Enter blindly in a form or while dropdown results load: it can submit. Observe and click the exact option. Scope duplicate labels to their section.

## Reuse answers with context

Separate deterministic facts from role-specific prose. An exact question is necessary but not sufficient for reusing prose: company, role, time window, jurisdiction, and source revision must also match. Recompose company-interest and project answers using the current posting and confirmed evidence. Do not transform a desired skill into claimed experience.

Keep a private answer index only where the project permits it: question text, semantic key, source reference, context, confirmation date, and last verification. Prefer references to profile fields over copying personal answers. Never place passwords, private answers, or demographic data in the shareable skill/plugin. User corrections invalidate affected cached answers.

When a new field wording has the same meaning as an existing confirmed fact, review it once and use the planner's `learn-alias` command to remember it. This is an operator review, not a new user-approval request. Do not learn paraphrases automatically from string similarity, unverified AI prose, or disclosure wording.

## Attachments and completion

Create the required role-specific resume using the authoritative template and supported PDF workflow; verify factual claims, page count/layout, company/role filename, and uploaded file. Preserve submitted versions. Read [ATS recipes](references/ats.md) for uploads and dynamic controls.

Read agreement wording and apply only the matching confirmed authorization. Do not equate consent, legal attestations, and factual eligibility. Follow employer AI-use rules. Unknown required facts remain unresolved rather than guessed; continue independent sections before requesting missing information.

Before any authorized submit, verify contact values, all required answers, both education entries when applicable, resume attachment, and current role/requisition. Follow the current host's submission requirements. Click submit at most once; require a portal receipt or explicit user-confirmed submission before marking Applied. If uncertain, investigate rather than retry. Update the existing tracker and application record, preserving evidence type.

## Performance and recovery

Optimize repeated reasoning and unnecessary tool round trips, not verification. Stop after two unsuccessful attempts on one control and inspect fresh UI or use one supported fallback. Save unresolved fields and continue the rest. Record actual elapsed time, section passes, corrections, and blockers if benchmarking; never promise extension-equivalent speed without measurements.

## Employment and skill corrections

Keep employment type separate from the display title. Explicitly label confirmed internships; do not relabel student employment or contract work as internships. A functional project heading is not evidence of a formal job title. AI-assisted prototyping does not establish independent programming or SQL proficiency. Apply corrections to future drafts and cached mappings while preserving submitted artifacts. Respect user-specific excluded essay topics from the private configuration, without making those exclusions universal.
