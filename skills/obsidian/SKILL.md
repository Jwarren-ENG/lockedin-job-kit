---
name: obsidian
description: Create, organize, refresh, or troubleshoot a private Obsidian job-search vault, including dashboards, application boards, interview calendars, task preservation and sync checks. Use for job-search vault work, not unrelated vaults.
---

# Maintain the job-search vault

Read [Obsidian reference](../../references/obsidian.md) and [tracking](../../references/tracking.md). Use the configured private workspace, never the plugin directory. An existing vault may use a different importer or schema: inspect its own instructions before choosing a tool.

## Establish the source of truth

1. Locate the requested vault, its Home note, existing instructions, importer and enabled plugins. Read only the relevant notes and configuration. Do not assume a previously used path still applies or create a second vault when one already exists.
2. Identify which records own application status, interviews, tasks and personal notes. In the bundled setup, SQLite owns applications, `interviews/*.json` owns appointments, and the exporter writes the private `obsidian` folder. The generated board is not a two-way status editor.
3. For a fresh bundled vault, run `python3 <plugin>/scripts/export_obsidian.py --workspace <private-workspace>`. For an existing custom vault, use its documented refresh process instead. Never run this exporter over an unrelated vault or silently migrate its layout.

## Work safely in existing notes

Preserve text outside managed markers, user properties, attachments, links and completed checkboxes. Update authoritative records first, then refresh managed views. Keep submitted resume artifacts unchanged. Do not replace a user's dashboard with a generic template just to change one section.

For organization requests, follow the user's established naming and folder conventions where possible. Keep a clear Home entrypoint and links to applications, interviews, calendar and skills. Move notes only with link reconciliation, and verify the resulting links resolve. A link-looking button is not working until opened in Obsidian.

The bundled exporter offers a Home note, generated application board and month interview calendar. It does not implement an interactive weekly task board, arbitrary existing-vault imports or automatic cloud sync. If requested, implement or configure those separately within the user's authorized scope and verify them before claiming support.

## Calendar and counts

Use one stable event ID per actual meeting, including standalone recruiter conversations without applications. Preserve the invitation evidence and explicit start/end offset or timezone. Update the same event on reschedule; cancelled meetings leave upcoming views but retain history. Do not infer completion merely because the scheduled time passed.

When a meeting appears twice, compare source records, event IDs and calendar providers before changing anything. Separate duplicate imports from distinct interviews for the same employer. Remove only a verified redundant managed entry, preserving notes. Repeated ICS imports can duplicate external calendar entries; the bundled ICS is a snapshot, not a subscription.

Check that Home's upcoming count equals the upcoming event set, the calendar includes that same set once each, and note links open correctly. Distinguish personal study tasks from employer deadlines. Preserve checked tasks and avoid recreating them as open tasks during refresh.

## Plugins and synchronization

Prefer core features when sufficient. Inspect installed plugins before adding another calendar, task or board provider. For requested enhancements, use official plugin distribution channels and the host's current authorization rules; do not install overlapping providers by default. Explain whether a board supports editing or is generated read-only.

Use the user's selected sync service and one sync system per vault. A local refresh, saved setting or connected account does not prove upload completion or second-device delivery. Check the service status and, where available, the same harmless note on the second device. If inaccessible, report local verification only. Never claim phone push notifications from vault sync; test notifications independently through the actual notification provider.

## Finish and report

After material changes, verify export success, note preservation, counts and visible navigation where UI access exists. Record any unchecked UI or remote-sync behavior. For scheduled runs, stay quiet when unchanged; report only material changes or a blocker requiring action. Keep profiles, demographic answers, credentials and full email bodies out of generated vault content.
