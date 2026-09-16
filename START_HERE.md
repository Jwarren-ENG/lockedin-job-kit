# Start your job search

## Get the apps

You need **one compatible assistant**, not every app below. Start on a computer; phone apps are useful for viewing synced notes and supported notifications.

| Tool | Official download or setup | Do I need it? |
|---|---|---|
| ChatGPT / Codex | [Download ChatGPT](https://chatgpt.com/download/) · [Codex](https://chatgpt.com/codex/) | Choose this or Claude. Use a desktop environment with local file access and the required tools. |
| Claude Desktop / Cowork | [Download Claude](https://claude.com/download) | Alternative assistant. Plugin and Cowork availability depends on your account. |
| Claude Code | [Official installation guide](https://code.claude.com/docs/en/quickstart) | Optional terminal-based alternative to the desktop apps. |
| Obsidian | [Download for computer, iPhone or Android](https://obsidian.md/download) | Optional: your job-search Home, notes, board and calendar. |
| Obsidian Sync | [Official Sync setup and plans](https://obsidian.md/sync) | Optional paid service for syncing the vault across devices. Not required for a local vault. |
| Python | [Download Python](https://www.python.org/downloads/) | The tracking helpers need Python 3.10+. Ask your assistant to check its existing runtime before installing anything. |

The setup form opens in your existing browser. Node.js and developer build tools are not needed to open it. Email connectors are connected inside your chosen assistant; the kit does not need your email password. Resume PDF creation uses the assistant's available LaTeX/PDF tools, which setup will check separately.

## Set up the kit

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

## Open your Obsidian dashboard

1. Install Obsidian from its official download page above.
2. Ask your assistant: “Create my Obsidian job-search vault.”
3. In Obsidian, choose **Open folder as vault** and select the generated `obsidian` folder inside your private workspace.
4. Open **Home**. Use **Application Board** and **Calendar** to browse your records.
5. For a column-style board, open **Settings → Community plugins → Browse**, find **Kanban**, and install and enable it. This is optional; the notes and calendar work without it.

To use the vault on your phone, install Obsidian there too and configure your chosen sync service. Use only one sync service for the vault. See [Obsidian details](references/obsidian.md) for refresh behavior and calendar limitations.

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
