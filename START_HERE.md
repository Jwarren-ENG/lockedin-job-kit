# Start your job search

1. Download the latest **job-search-kit.zip** from this repository's Releases and unzip it. Keep the folder named `job-search-kit`. You don't need to build the interface.
2. Open **assets/setup.html** in your browser. Fill in your details, target roles and permissions. All choices start off. Download your private setup file somewhere outside this repository.
3. Open the kit in your assistant using an option below. Attach your resume (LaTeX preferred), and your downloaded setup file through the assistant's normal file controls.
4. Paste this:

> Read skills/start/SKILL.md and set up Job Search Kit for me. Use my attached setup and resume. Save my private workspace outside this code folder. Confirm my resume facts, test available tools, create my tracker, and offer an Obsidian board and calendar. Ask me about anything missing. Configure daily searches and email tracking only according to my permissions. Show me what is ready and what still needs connecting.

## Choose your assistant

**Codex desktop:** Open the unzipped folder as a project and paste the prompt above. This folder-based route works without registering a marketplace. The included Codex plugin manifest can also be installed through a compatible custom marketplace/share flow. Open a fresh task after installation. See [host details](references/hosts.md).

**Claude Code:** From the unzipped folder run `claude --plugin-dir .`, then `/job-search-kit:start`.

**Claude Desktop / Cowork:** Use its custom plugin upload flow to upload the release ZIP or `.plugin` file, if your account supports it. Otherwise, grant Cowork access to the unzipped folder and use the prompt above. Select a separate private folder for your data.

Normal web chat without local tools cannot operate this full workflow. Browser control, email, PDF generation and scheduling are provided by your assistant, not by this download.

## Before your first application

The assistant will confirm your name, contact links, education, experience, work authorization, location, start date and role preferences. Unknown answers stay unknown. Optional demographic information is collected only if you choose to save it. Passwords belong in your password manager.

Start with a draft application so you can inspect the resume and answers. Enable automatic submission only if you want it. Unfamiliar personal questions, account security steps and missing facts still need your input. Completed forms count as drafts until there is submission evidence.

## Daily use

- “Find new jobs matching my profile.”
- “Prepare these applications for review.”
- “Check job emails and update my tracker.”
- “Create my Obsidian vault and calendar.”
- “Show me skills to practice for these roles.”
- “Pause my job search.”

Daily monitoring runs through your assistant's scheduler. Keep its required device/runtime available. Test notifications on each device; a saved schedule is not proof of a phone alert. The kit does not install a background service.
