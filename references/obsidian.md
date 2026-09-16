# Optional Obsidian workspace

Ask the assistant: “Create my Obsidian job-search vault.” It runs:

```sh
python3 scripts/export_obsidian.py --workspace /path/to/private-workspace
```

Open the generated `obsidian` folder as a vault in Obsidian. Home, application notes and a month calendar work with core Obsidian. For columns, install the optional **Kanban** community plugin from Obsidian's own catalog and open Application Board. No community plugin code is bundled or silently installed.

The board is a generated view of the tracker, not a two-way editor. Ask the assistant to change application status, then refresh. Keep personal notes below “My notes” in application/interview notes; the exporter preserves them. Manual changes inside managed sections or the generated board are replaced. Refresh after each search or email update.

Save confirmed interview records in the private workspace's `interviews/` folder, one JSON file per stable event ID:

```json
{"id":"example-interview","company":"Example Employer","role":"Analyst","status":"Scheduled","start":"2030-06-10T14:00:00-04:00","end":"2030-06-10T14:30:00-04:00","format":"Video call"}
```

Use the invitation's date, timezone and offset, including daylight saving time. Preserve its evidence in the private record. Update the same ID when rescheduled. Set status to Cancelled or Completed as appropriate; it will leave upcoming counts and the current calendar export. Duplicate IDs are rejected. Past notes are retained as history. Email arrival time is not interview time.

`Interviews.ics` is a calendar snapshot, not a live subscription. Repeated imports into another calendar may duplicate events, and removed events are not automatically deleted there. The in-vault Calendar always reflects the latest export.

Sync is optional and user-configured. Choose one supported service, such as Obsidian Sync. Never configure two sync systems for the same vault. Verify on the user's second device before claiming phone sync. The plugin cannot promise phone push notifications; test the host's notification channel separately.

Only selected application fields are exported. Profiles, demographic answers, addresses, resumes and email bodies are not copied to the vault by this helper. User-authored job fields and notes can still contain private information: treat the vault as private.
