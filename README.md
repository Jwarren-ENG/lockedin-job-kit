# Job Search Kit

Bring a résumé and one job posting. The kit helps you decide whether a job fits, tailor a résumé you can stand behind, and remember what happened after you applied.

## Try it in your first chat

1. Open [ChatGPT](https://chatgpt.com/) or [Claude](https://claude.ai/). Use a private chat or a project only you can access.
2. Attach your résumé with the **+** button, or paste the experience you want to use. Paste the employer’s job description if you have it handy.
3. Open the [starter instructions](CHAT_STARTER.txt), copy the text into your message, and send it. You can also [download the starter as a text file](https://github.com/Jwarren-ENG/job-search-kit/releases/latest/download/CHAT_STARTER.txt) and attach it. The same instructions work in other assistants that accept pasted text.

Your first result should tell you which job requirements you can demonstrate, flag unanswered questions and give you a résumé edit you can review. You choose what to send to an employer. Everything above works by copying and pasting, including on a phone.

| What would you like to do? | Where to go |
| --- | --- |
| Try one application in ChatGPT or Claude | [Follow the steps for your app](START_HERE.md#use-a-chat) |
| Keep working on your search in future chats | [Save your search](START_HERE.md#keep-your-search-between-chats) |
| Let an assistant with computer access maintain files or help fill a form | [Set up the desktop kit](START_HERE.md#set-up-the-desktop-kit) |
| See upcoming interviews in Obsidian | [Open your dashboard](START_HERE.md#open-your-obsidian-dashboard) |

## What to ask next

* **Compare openings.** “I want a remote operations job in my state. Compare these two postings. Show the posted base salary and any travel requirement.”
* **Review an application.** “Show me the exact résumé wording you changed and the experience that supports each change.”
* **Update the tracker.** “I received a first round interview invitation. Here is the role and date. Add it to my tracker and help me prepare.”
* **Pick up tomorrow.** “Give me a short search summary and an updated tracker I can save for our next chat.”

## What the desktop kit adds

The [full download](https://github.com/Jwarren-ENG/job-search-kit/releases/latest/download/job-search-kit.zip) includes a setup form that opens on your computer, a blank résumé template and a tracker. A compatible assistant can keep a copy of the exact résumé used for each application, check for duplicates, and export a spreadsheet or Obsidian dashboard. Browser access, email and scheduled searches each depend on the tools available in your app and the permissions you give it. [Desktop setup and permissions](START_HERE.md#set-up-the-desktop-kit)

## Share the kit

Share the clean starter file or the release ZIP. Keep your completed setup file, résumés, tracker and interview links in your own private folder. If someone opens your link and sees a GitHub sign-in or 404 page, they may need repository access. You can send them a clean copy of the starter text directly. [Privacy guide](PRIVACY.md)

## For maintainers

The [host guide](references/hosts.md) covers plugins and scheduling. The [test guide](TESTING.md) lists verification commands and runtime requirements. To build a release, run the Python tests, the release audit and `python3 scripts/package.py dist`. Include new distributable files in `release-files.json`. [License](LICENSE) · [Component attribution](ui/SHADCN-LICENSE.md)
