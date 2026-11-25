---
name: status
description: Review job application progress, process authorized recruiter emails, record interviews or outcomes, and refresh the application spreadsheet.
---

# Status and responses

Read [tracking](../../references/tracking.md) and current permissions. A user-reported interview or submission is valid evidence when labeled user-confirmed; do not demand an email to record it. Dates without a time do not establish a time zone or meeting time.

When read_email is granted, use the explicitly selected mailbox/account through a supported connector. Search relevant employer/requisition threads with overlap since the last successful mail checkpoint. Read complete relevant bodies; distinguish new text from quoted content. If search coverage is partial, narrow by mailbox/date and record the actual coverage. Do not mark a full inbox check complete when only one employer was searched.

Use stable RFC Message-ID or provider IDs for event deduplication. Match employer plus role/requisition before applying an outcome; an unrelated rejection from the same employer is not a match. Distinguish receipt, assessment, interview invitation, scheduled interview, rejection, offer and withdrawal. Keep meeting date/time and scheduling-needed status in notes/next_action. Save relevant evidence, deadline and contact, not unrelated messages.

Use `jobkit.py status <id> <state> --evidence <evidence> --event-key <stable-id> --next-action <action>` and then refresh the workbook. A receipt arriving after an interview must not regress the application to Submitted. If events conflict, record the conflict and ask rather than silently overriding. Never infer rejection from silence or accept an offer, schedule a meeting, send replies or withdraw on status-monitor permission alone.

Report next actions and actual evidence. Run interview-prep when requested. Pause/revoke requests take effect immediately: `jobkit.py pause` blocks future application reservations; also pause/delete the matching native schedule through host tools when authorized. Disabling a connector permission should end that use immediately.

When the current obsidian_export permission is enabled, use [the Obsidian skill](../obsidian/SKILL.md) to refresh the existing vault after source updates and verify Home/calendar consistency. Local refresh does not verify remote sync.
