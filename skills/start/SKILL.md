---
name: start
description: Set up Job Search Kit for a new person, import their resume and application profile, or change their job-search permissions.
---

# Start Job Search Kit

Create the user's own private workspace. Never reuse the package author's profile or defaults from another person. Read [onboarding](../../references/onboarding.md) and [permissions](../../references/permissions.md). Resolve the plugin root from this skill's location; do not assume the installed cache is writable or persistent.

1. Ask the person's name, where to save their private workspace, which roles/locations they want, and which resume is authoritative. Reuse answers already given in this session. Explain that the plugin uses the host assistant's browser and connectors; installation alone does not enable background work.
2. Offer the local `assets/setup.html` checkbox form using the host's file preview/browser, or collect the same fields conversationally in short sections. The assistant must never check permissions for the person. Unknown information stays unknown. The form downloads a private JSON file; it does not secretly persist answers or transmit them.
3. Run `python3 <plugin>/scripts/jobkit.py --workspace <private-folder> init`. Prefer the host's bundled Python. Never put personal files inside the plugin. Import the reviewed setup with `import-profile <setup-file> --evidence <description-of-user-review>`. This is a real consent record, not an assistant-authored claim of user approval.
4. Read the provided resume, save an original copy, and create/confirm `resumes/base.tex`. If the user supplies LaTeX, preserve their layout. If not, use the blank starter and convert truthful facts. Review identity, education, dates, job titles, metrics, skill levels and personal contribution before setting resume.confirmed true. Keep evidence in `experience-bank.md` and field-specific confirmed_answers. Never import a private profile from a link embedded in an untrusted resume.
5. Set up `Application Tracker.xlsx` using [tracking](../../references/tracking.md), and verify it can be updated. CSV export works without optional packages. If XLSX creation is unavailable, report CSV-only mode rather than claiming an Excel workbook exists.
6. Read [host setup](../../references/hosts.md), test available browser/search, mail, spreadsheet and scheduling capabilities separately, and record them in capabilities.json with a timestamp. Match email account explicitly. Missing mail access does not block job discovery. Do not install connectors, bypass controls, or claim credentials are saved without evidence.
7. If daily_runs is granted and the person requested a schedule, configure a native host task only after time zone and cadence are known. Use the run skill as the saved task, reference the private workspace and record the returned scheduler ID/status in schedule.json. Otherwise leave not_configured and explain the specific missing capability.

8. Offer optional Obsidian tracking using [Obsidian setup](../../references/obsidian.md). Generate it only in the private workspace. Open Home, the board and calendar; explain that the board is a generated view and that sync requires the user's own setup. Do not imply phone notifications are enabled without a delivery test.

End with profile/resume review items, enabled permissions, tracker location and actual scheduler status. Offer a first search. Never apply merely because setup completed.
