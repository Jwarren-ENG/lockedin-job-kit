# Privacy and publication

The public repository contains blank templates, reusable skills, source code and fictional tests. Each applicant's private workspace must be outside the repository. The setup form makes no network requests and downloads a local file; importing it into an assistant is a separate action subject to that host's data policy.

Do not commit profiles, resumes, addresses, optional demographic answers, email content, recruiter conversations, calendar invitations, application answers, receipts, credentials or private workspace backups. The ignore rules help prevent mistakes, but are not a security boundary. Never force-add ignored private files.

Before every release:

1. Review the exact files in `release-files.json` and the staged Git diff.
2. Run the tests and release audit. It checks file paths, common secret formats, machine paths and unexpected tracked files, but cannot detect all personal information.
3. Scan the staged content for the author's personal contact details and private project identifiers using a local check that is not committed.
4. Generate archives with `scripts/package.py`; do not zip a working directory or private workspace.
5. Use a generic contributor name and a non-personal commit email if keeping personal identity out of commit metadata matters. A public repository's owning GitHub account remains visible.

No telemetry, hosted database, password store or shared applicant account is included. Local data is not encrypted by this kit. Use your operating system's protections and your password manager. Email and web operations happen only through the host tools you connect and authorize.

Do not include private setup files or resumes in GitHub issues. Report bugs with fictional, minimal examples.
