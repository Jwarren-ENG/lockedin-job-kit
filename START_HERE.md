# Start your job search

## Use a chat

Have your latest résumé and one job description ready. If you are still writing your résumé, a few lines describing your work and education are enough to begin.

### ChatGPT

1. Open [ChatGPT](https://chatgpt.com/) and start a new private conversation.
2. Select **+** next to the message box, choose **Add photos & files**, and select your résumé. You can also paste the relevant parts.
3. Copy the [starter instructions](CHAT_STARTER.txt) into the message. Underneath, paste the job description or the employer’s link. If ChatGPT cannot open the link, paste the description. Send the message and answer any questions about your goals. [ChatGPT file help](https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt)

### Claude

1. Open [Claude](https://claude.ai/) and start a new private conversation.
2. Select **+**, choose **Add files or photos**, and attach your résumé. You can drag it into the chat on a computer.
3. Paste the [starter instructions](CHAT_STARTER.txt) and a job description. Send them together. If your résumé is on another device, paste a short work history for now. [Claude file help](https://support.claude.com/en/articles/8241126-upload-files-to-claude)

### Another chat app

Paste the same starter text, your work history and the job description into a private conversation. If the app cannot browse, supply the text and date from the employer’s page yourself.

**What a first result looks like.** Suppose a posting asks for Excel and weekly reporting. Your résumé says you prepared a weekly inventory report in Excel. A good first draft keeps both details. If the posting also asks for SQL and your résumé is silent, the assistant should ask whether you have used it. Read the proposed wording before using it.

## Keep your search between chats

At the end of a session, ask for a tracker you can save. A spreadsheet or a table in a note is enough. Keep the employer, role, posting link, current stage and exact résumé filename on each row. If you apply yourself, tell the assistant when you submitted or share the relevant part of the confirmation. An interview invitation and a scheduled interview are different stages.

For repeat use in ChatGPT, create a private **Project** named *My Job Search*, add the starter text and your résumé to its sources, and start your next chat there. In Claude, add those files to the **Files** section of a private project if your account offers Projects. Keep the latest tracker there as well. You can also attach your saved tracker and starter to a fresh chat. [ChatGPT projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) · [Claude projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)

## Set up the desktop kit

Choose this route if you want a private folder of application files, a spreadsheet that the assistant can update, or an optional Obsidian dashboard.

### Optional downloads

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

### Open the setup form

1. Download the [desktop ZIP](https://github.com/Jwarren-ENG/job-search-kit/releases/latest/download/job-search-kit.zip) and unzip it. If your computer asks where to extract it, choose a new folder called `job-search-kit`. You don't need to build the interface.
2. Open **assets/setup.html** in your browser. Fill in your details, target roles and permissions. All choices start off. Download your private setup file somewhere outside this repository.
3. Open the kit in your assistant using an option below. Attach your existing résumé, and your downloaded setup file through the assistant's normal file controls.
4. Paste this:

> Read skills/start/SKILL.md and set up Job Search Kit for me. Use my attached setup and resume. Save my private workspace outside this code folder. Confirm my resume facts, test available tools, create my tracker, and offer an Obsidian board and calendar. Ask me about anything missing. Configure daily searches and email tracking only according to my permissions. Show me what is ready and what still needs connecting.

### Open the kit in your desktop assistant

**Codex desktop:** Open the unzipped folder as a project and paste the prompt above. This folder-based route works without registering a marketplace. The included Codex plugin manifest can also be installed through a compatible custom marketplace/share flow. Open a fresh task after installation. See [host details](references/hosts.md).

**Claude Code:** From the unzipped folder run `claude --plugin-dir .`, then `/job-search-kit:start`.

**Claude Desktop / Cowork:** Use its custom plugin upload flow to upload the release ZIP or `.plugin` file, if your account supports it. Otherwise, grant Cowork access to the unzipped folder and use the prompt above. Select a separate private folder for your data.

Ask your desktop assistant to show which tools it can use in this session. If an option is unavailable, you can still use the chat steps above and save the tracker yourself.

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
