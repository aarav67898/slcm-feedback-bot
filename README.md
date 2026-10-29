# MUJ SLCM Feedback Helper

A small Python + Selenium helper for the Manipal University Jaipur SLCM feedback page.

It is designed to:
- Open SLCM in Chrome and let you sign in yourself.
- Select **YES** for unanswered YES/NO radio groups.
- Set visible dropdowns to **Yes** only when their current value is the placeholder (`Select` / blank).
- Leave comments fields untouched.
- Leave existing answers unchanged.
- **Never click Submit**. You review and submit each questionnaire yourself.

> **Important:** Feedback should reflect your genuine experience. Review every answer before submitting. The page's HTML can change, so test on one questionnaire first.

## Requirements

- Windows 10/11 (other platforms may work)
- Python 3.10 or newer
- Google Chrome
- Internet access for Selenium to obtain a compatible driver if needed

## Setup on Windows

Open Command Prompt in this project folder and run:

```bat
py --version
py -m pip install -r requirements.txt
```

If `py` is not recognized, install Python from [python.org](https://www.python.org/downloads/windows/) and enable the option to add Python to PATH. Open a new Command Prompt afterwards.

## Run

```bat
py slcm_feedback_bot.py
```

1. Chrome opens the SLCM login page.
2. Sign in manually.
3. Open one pending feedback questionnaire.
4. Return to the terminal and press Enter.
5. The helper fills eligible unanswered controls and prints a summary.
6. Review the answers in Chrome and submit the form yourself.
7. Navigate manually to the next questionnaire, then type `NEXT` in the terminal. Type `QUIT` to stop.

The helper does not store your password or access credentials.

## What it changes

### YES/NO radio groups
The helper groups radio inputs by their `name` attribute. If a group already has a selected option, it leaves it alone. Otherwise, it looks for a radio whose enclosing label text is `YES` and clicks that label.

### Dropdowns
For visible, enabled `<select>` elements, it selects `Yes` only if the current selected text is `Select` or blank and an option labelled `Yes` exists. A dropdown with a pre-existing Yes/No response is left unchanged.

### Comments
Comments are not filled, cleared, or modified.

## Troubleshooting

- **No questions found:** Confirm that the questionnaire is open and its questions are visible before pressing Enter.
- **Could not select an option:** The site may have changed its HTML or may use a different control structure. Inspect the relevant element in Chrome DevTools and update the selectors carefully.
- **Chrome/driver error:** Update Chrome and retry. Selenium Manager normally manages the compatible driver automatically.
- **Wrong dropdown was targeted:** The helper considers any visible dropdown with a `Yes` option whose current value is `Select`/blank. Review the page before submission.

## GitHub

From inside this folder:

```bat
git init
git add README.md requirements.txt slcm_feedback_bot.py .gitignore LICENSE
git commit -m "Add SLCM feedback helper"
```

Create an empty repository on GitHub, then follow GitHub's instructions to add the remote and push.

**Never commit passwords, cookies, session tokens, personal student information, or screenshots containing private details.**

## Disclaimer

This is an unofficial, personal automation helper and is not affiliated with Manipal University Jaipur. Use it only in accordance with your institution's policies and the website's terms. You are responsible for reviewing all answers and deciding whether to submit them.
