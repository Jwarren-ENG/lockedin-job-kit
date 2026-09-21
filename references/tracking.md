# Tracking and spreadsheet updates

`applications.sqlite` is the canonical machine log. `exports/applications.csv` and `.json` are automatically regenerated after every job/status/reservation update. The CSV opens in Excel, Numbers and Google Sheets and escapes formula-leading text. Personal identity, permissions and demographics are excluded. Do not include credential links in notes. The CSV is generated: manual edits should be reconciled through job records before another export.

The user-facing workbook is `Application Tracker.xlsx` in the private workspace. Use the host's spreadsheet skill/tool when available. A portable helper `scripts/export-workbook.mjs` uses the documented @oai/artifact-tool runtime when available; resolve the host-bundled Node/dependencies without installing into plugin caches. If unavailable, use the host's permitted spreadsheet authoring method, or explicitly report CSV-only mode. Never silently replace an existing workbook with a regenerated one that loses user notes.

For Google Sheets, first obtain a user-chosen private spreadsheet or permission to create one. Use the connected provider's sheet API and store the real document ID/link in capabilities.json. Patch only matching stable-ID rows; preserve user notes and unrelated tabs. No Google connector is bundled, and an emailed CSV is not a live Sheet.

Tracker columns: stable ID, company, role, location, official URL, requisition, salary min/max/currency/period, posted date, first seen, current status, submitted date, next action, deadline, recruiter contact, resume, notes, skill gaps and evidence. Preserve unknowns. Count submissions by recorded submission date or event history, not only current status; interview/rejection does not erase a prior submission. Do not invent submission dates when a user reports an interview without knowing when they applied.

Append evidence-backed events. `status` uses event-key for mail deduplication; use provider/RFC message ID plus event kind where a message contains multiple updates. Do not regress a later stage when an old receipt arrives. Store both event time and scheduled interview time in notes or the job record; never relabel email arrival as appointment time. Programmatic helper validates record transitions but the agent must resolve semantic order and evidence.

After every run check database/export agreement, workbook updated rows and totals, visual legibility when applicable. On export failure, keep canonical application events and mark workbook refresh pending; do not retry an external submit. Keep logs of per-source and per-mailbox checkpoints, failure, completeness and deduplicated notifications.

The provided workbook helper creates a Tracker table on first use and subsequently updates only plugin-owned columns on that sheet. The Notes column is user-owned after creation. It never removes missing rows or changes other tabs. Reconcile user edits before overwriting any other column; use manual mode if the workbook no longer matches its headers.

## Coverage checkpoints and quiet runs

Use separate schedules and checkpoints for job discovery and each mailbox. More frequent job searches do not authorize repeated email scans. Verify the connected account identity before reading. For large mailboxes, use bounded folder/date searches; partial or timed-out results cannot support a no-mail conclusion or advance that search checkpoint.

A recent-message fallback can establish coverage only if its ordered date range spans the intended overlap. Record its actual range, pagination and limitations separately from failed searches. Read relevant messages fully, deduplicate RFC Message-ID across accounts, and distinguish LinkedIn notification previews from full recruiter conversations.

Log routine coverage in one structured run record rather than repeatedly appending identical prose to status pages. Update status notes and workbook rows for material changes. Record unchanged workbook verification separately from edits. A local Obsidian import is not proof of cloud sync, fresh email access or live job discovery. Preserve standalone interviews, completed preparation tasks, and original invitation evidence; deduplicate reschedules and cancellations by event identity.
