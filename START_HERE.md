# Open #LOCKEDIN Job Kit in your app

## Use a chat

Choose the [Beginner guide](BEGINNER.md), [Advanced guide](ADVANCED.md) or [Local guide](LOCAL.md). Have your latest résumé or work history handy. The kit first reads the résumé and asks you to confirm what it found. You then choose whether any specific past chat may supply extra context. It asks about the work you want and any remaining application details afterwards. If you are still writing your résumé, a few lines describing your work and education are enough to begin.

### ChatGPT

1. Open [ChatGPT](https://chatgpt.com/) and start a new private conversation.
2. Select **+** next to the message box, choose **Add photos & files**, and select your résumé. You can also paste the relevant parts.
3. Copy the [starter instructions](CHAT_STARTER.txt) into the message. A job description or an employer’s link is optional. If ChatGPT cannot open the link, paste the description. Send the message and answer any questions about your goals. [ChatGPT file help](https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt)

### Claude

1. Open [Claude](https://claude.ai/) and start a new private conversation.
2. Select **+**, choose **Add files or photos**, and attach your résumé. You can drag it into the chat on a computer.
3. Paste the [starter instructions](CHAT_STARTER.txt) and send them. Add a posting if you already have one. If your résumé is on another device, paste a short work history for now. [Claude file help](https://support.claude.com/en/articles/8241126-upload-files-to-claude)

### Another chat app

Paste the same starter text, your work history and the kind of job you want into a private conversation. If the app cannot browse, supply the text and date from the employer’s page yourself.

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

1. Download the [desktop ZIP](https://github.com/Jwarren-ENG/lockedin-job-kit/releases/latest/download/job-search-kit.zip) and unzip it. If your computer asks where to extract it, choose a new folder called `job-search-kit`. You don't need to build the interface.
2. Open **assets/setup.html** in your browser. Start by pasting your résumé text or choosing a text file. Check the extracted facts, then step through the missing details and permissions. You can paste from a PDF or Word file, or use the assistant to read the original attachment. All choices start off. Download your private setup file somewhere outside this repository.
3. Open the kit in your assistant using an option below. Attach your existing résumé, and your downloaded setup file through the assistant's normal file controls.
4. Paste this:

> Read skills/start/SKILL.md and interview me to set up #LOCKEDIN Job Kit. Use my attached setup and resume. Save my private workspace outside this code folder. Confirm my resume facts, test available tools, create my tracker, and help me choose sources for the role I want. Ask me about anything missing. Configure daily searches and email tracking only according to my permissions. Show me what is ready and what still needs connecting.

### Open the kit in your desktop assistant

**Codex desktop:** Open the unzipped folder as a project and paste the prompt above. This folder-based route works without registering a marketplace. The included Codex plugin manifest can also be installed through a compatible custom marketplace/share flow. Open a fresh task after installation. See [host details](references/hosts.md).

**Claude Code:** From the unzipped folder run `claude --plugin-dir .`, then `/job-search-kit:start`.

**Claude Desktop / Cowork:** Use its custom plugin upload flow to upload the release ZIP or `.plugin` file, if your account supports it. Otherwise, grant Cowork access to the unzipped folder and use the prompt above. Select a separate private folder for your data.

Ask your desktop assistant to show which tools it can use in this session. If an option is unavailable, you can still use the chat steps above and save the tracker yourself.

## Open your Obsidian dashboard

If you want interview notes and a calendar in Obsidian, follow the [optional setup guide](OPTIONAL_OBSIDIAN.md). You can keep using the spreadsheet alone.

## Before your first application

The assistant will confirm your name, contact links, education, experience, work authorization, location, start date and role preferences. Unknown answers stay unknown. Optional demographic information is collected only if you choose to save it. Passwords belong in your password manager.

Start with a draft application so you can inspect the resume and answers. Enable automatic submission only if you want it. Unfamiliar personal questions, account security steps and missing facts still need your input. Completed forms count as drafts until there is submission evidence.

## Daily use

Before setting a daily pace, open the [workload planner](docs/index.html). Set applications per active day and days per week. Try the turns, tokens and review minutes you observed on one real application. Use the same reset window if you compare with an account allowance.

### Estimate what one application costs

If you pay for model usage, add up the uncached input and billed output tokens across all calls for one application. Multiply each count by its rate, add the two amounts, then divide by one million. For example, 3,000 input and 600 output tokens on GPT-6.2 Sol cost $0.012 through the API. The same workload uses 0.3 purchased Codex credits at Standard speed. Your subscription dashboard gives your included limits and reset times.

These starting rates were checked on November 25, 2026. Each column gives the rate per million tokens. The OpenAI API examples use Standard pricing for individual requests with up to 272,000 input tokens.

| Model and billing method | Input | Output | Official rate card |
| --- | ---: | ---: | --- |
| GPT-6.2 Sol API | $2 | $10 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-6.2-sol) |
| GPT-6.2 Astra API | $8 | $40 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-6.2-astra) |
| GPT-6 Luna API | $0.10 | $0.50 | [OpenAI](https://developers.openai.com/api/docs/models/gpt-6-luna) |
| Claude Sonnet 5.5 API | $2 | $10 | [Anthropic](https://platform.claude.com/docs/en/about-claude/pricing) |
| Gemini 4 Neon API | $3 | $15 | [Google](https://ai.google.dev/gemini-api/docs/pricing#gemini-4-neon) |
| GPT-6.2 Sol purchased credits | 50 credits | 250 credits | [Codex](https://developers.openai.com/codex/pricing/) |
| GPT-6.2 Astra purchased credits | 200 credits | 1,000 credits | [Codex](https://developers.openai.com/codex/pricing/) |

You can edit every rate. For an unlisted model, choose **Other API model** and leave unconfirmed prices blank. Tool charges, caching and special service tiers need their own billing details.

For local runs, multiply measured average watts by active model minutes per application, divide by 60,000 to get kWh, then multiply by your electricity rate in USD per kWh. At the example 60 W and 2 to 6 minutes, one job uses 0.002 to 0.006 kWh. At the September 2026 US residential average of $0.1817 per kWh, that costs $0.0003634 to $0.0010902. Replace the examples with a wall meter reading, timed model use and the rate from your bill. [EIA Table 5.6.A](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a)

### Requests you can make

- “Find new jobs matching my profile.”
- “Prepare these applications for review.”
- “Check job emails and update my tracker.”
- “Create my Obsidian vault and calendar.”
- “Show me skills to practice for these roles.”
- “Pause my job search.”

Daily monitoring runs through your assistant's scheduler. Keep its required device/runtime available. Test notifications on each device; a saved schedule is not proof of a phone alert. The kit does not install a background service.
