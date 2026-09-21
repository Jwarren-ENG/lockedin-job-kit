# Job Search Kit

A shareable assistant plugin for personalized job searches, truthful LaTeX resumes, application tracking, consent choices and interview preparation.

## Start in a few minutes

Download the ZIP from **Releases**, unzip it, and follow [START_HERE.md](START_HERE.md). The included setup form uses React and shadcn/ui and runs locally without a build or server.

Need the apps first? [Download Obsidian](https://obsidian.md/download), [ChatGPT](https://chatgpt.com/download/), or [Claude](https://claude.com/download). The [setup guide](START_HERE.md#get-the-apps) explains which tools are required and which are optional, including Python, Obsidian Sync and the Kanban plugin.

## Start

Install the plugin in a compatible host, then say:

> Start Job Search Kit. Ask me for my details, resume, target roles and permissions, and set up my private job-search workspace.

Claude Code also supports `/job-search-kit:start`. For local testing use `claude --plugin-dir /absolute/path/to/job-search-kit`. In Claude Desktop/Cowork, use the custom-plugin upload flow with the ZIP or `.plugin` package where supported. In Codex, use the plugin's marketplace/share flow, then open a new task. Installation alone does not authorize applications.

## Included

- A local setup form with real permission checkboxes and private JSON export.
- Guided collection of name/contact links, addresses, education/experience, eligibility, salary/location/role preferences and an authoritative resume.
- A blank LaTeX starter for people without a template; preserve an existing template when supplied.
- SQLite application history with stable IDs, duplicate detection, submission reservations, evidence and daily caps.
- Automatically refreshed CSV/JSON tracker; an Excel workbook helper when the host has its supported spreadsheet runtime. Google Sheets can be connected through the host.
- Optional Obsidian Home, application board, month calendar and interview calendar export.
- APM List and Jobright new-grad PM discovery sources, filtered to each user.
- Six skills: start, run, apply, job-application-autofill, status and interview-prep.
- Native-host daily scheduling instructions and mailbox checkpoint/deduplication workflow.
- Separate permissions for automatic submissions, account creation, email reads, recruitment privacy, talent pools, recruiting partners, AI notes, and demographic storage/disclosure.

## What runs where

The assistant researches and operates application pages using its connected tools. Local helpers maintain state; they do not contain an ATS browser bot or scrape email. Python 3.10+ is required for the tracking helpers, with no third-party Python dependencies. Excel helper needs Node and @oai/artifact-tool, normally supplied by a capable host; otherwise use its spreadsheet tool or the included CSV. PDF generation requires the host's LaTeX/PDF tools. Daily operation requires a configured native scheduler and the host's runtime/access conditions.

No cross-host login, CAPTCHA bypass, automatic connector installation or hidden background service is included. Each user's host account and permissions determine what can run unattended. Unfamiliar required answers or restrictions produce a saved draft and a clear request for user action.

## Private data and sharing

Choose a private workspace outside the plugin. The package ships blank. Do not place your profile, demographics, mail, application records, resumes, credentials or private setup exports into the plugin folder. Local files are not encrypted by this plugin; use appropriate filesystem/account protections. Host data processing policies still apply. Unique passwords stay in your password manager.

To share, send only the supplied clean package. The release script packages an explicit source allowlist and rejects suspicious private-data files. Do not zip your private workspace. Existing employer disclosures cannot be undone by changing a checkbox. “Pause my job search” stops new actions and asks the host to pause the schedule.

## Usage

- “Run my job search now.”
- “Show me the applications awaiting approval.”
- “Apply to this role using my saved permissions.”
- “Check job responses and refresh my tracker.”
- “Turn off partner sharing and auto-submit.”
- “Prepare me for this interview next Tuesday.”

## Validation and scope

See TESTING.md for actually executed tests. The first release provides executable local tracking and agent workflows; a successful local test is not proof that every employer portal or every host integration works. Test a draft on your own connected host before enabling unattended submissions. Version 0.2.1.

## Development and sharing

Python 3.10+ is enough for core tracking and Obsidian exports. Run `python3 -m unittest discover -s tests -v`, then `python3 scripts/audit_release.py` and `python3 scripts/package.py dist`. Release archives use an explicit file allowlist. New source files must be added to `release-files.json`. See [privacy boundaries](PRIVACY.md) and the MIT [license](LICENSE). The shadcn attribution remains in `ui/SHADCN-LICENSE.md`.

## v0.3.0

Includes the section-level autofill planner and fictional-data regression tests. Routine fields resolve from confirmed private facts; novel answers remain grounded drafts. Improved guidance covers internship labels, AI-assisted skill depth, confidential projects, stale postings, mailbox coverage and quiet scheduled runs. The planner does not operate or submit browser forms by itself.
