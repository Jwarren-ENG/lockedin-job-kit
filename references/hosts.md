# Host setup and honest capability reporting

This is a skill plugin with local tracking helpers. It does not include a browser extension, email credentials, model subscription or standalone always-on application bot. A compatible host assistant executes the skills with tools the user connects. Test those capabilities independently.

## Codex desktop

Install from the personal marketplace/share flow or a user-configured marketplace. Start a new task after installation and ask to use job-search-kit. Use available browser tools, connected email provider and spreadsheet/PDF skills. For requested recurrence, discover the native automation tool and prefer a thread heartbeat. Inspect existing automation first and extend the matching job-search monitor rather than duplicating it. If one task permits one heartbeat, combine authorized job search and email tracking. Respect quiet/no-change output requirements. Verify the returned schedule ID/status before reporting active. A plugin file cannot itself schedule runs.

## Claude Code

The package contains `.claude-plugin/plugin.json` and namespaced skills. For local testing, `claude --plugin-dir /absolute/path/to/job-search-kit` then `/job-search-kit:start`. Browser/mail require the user's installed tools. Do not assume computer use or scheduling exists in a CLI session. If a native scheduler is unavailable, leave manual mode and explain it; do not create a system daemon or assume the app remains running.

## Claude Desktop / Cowork

Use the host's custom-plugin upload flow for the supplied ZIP or `.plugin` archive if supported by the account. Ask to run Job Search Kit setup or select its start skill. Select a private writable folder through Cowork's access controls. The plugin's installed cache is not the user's data folder. Verify supported browser, email and spreadsheet tools before use. If the host has native scheduled tasks, configure one only with consent and a confirmed schedule. The scheduler's runtime/access requirements apply; label unavailable features clearly.

## Other Claude interfaces

A normal chat without plugin support, local file access, browser controls or a scheduler cannot run the entire workflow. It can help with profile review and resume text; do not label that as an installed or automated plugin. Never claim the same tool names or runtime paths work across all hosts.

## Daily prompt template

Run one Job Search Kit cycle for the user's private workspace using its current profile and permissions. Check configured sources for new matching openings, verify official postings, deduplicate, tailor resumes and submit only when authorized and all required facts are confirmed. Process job-related email only if permitted in the selected account. Update application records, spreadsheet, skill gaps and coverage checkpoints. Do not bypass host controls or retry uncertain submissions. Notify meaningful new matches, verified submissions, employer responses, deadlines and user-action blockers; stay quiet when unchanged. Re-read pause/revocation state before external actions.

## Capability record

For browser, search, email, latex, PDF review, spreadsheet and scheduler, record available/unavailable/untested, tool/provider, selected account/workspace, checked_at and limitation. A discovery result is not a successful end-to-end test. Do not put secrets or authentication URLs in this file.

Official format references checked while building v0.1.0: https://code.claude.com/docs/en/plugins and https://support.claude.com/en/articles/13837440-use-plugins-in-claude. Codex format follows the local plugin-creator manifest validator. Host interfaces may change.
