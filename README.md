# job-mail-alert 📬

This is my first project that uses a real API. I'm a 2nd year Computer Science student and I was looking for a part-time job, but the job emails were getting lost between newsletters, bank emails and university emails. So I wanted a small program that reads my inbox, finds only the important emails and sends me one summary email.

At first I built it only for job emails, but then I thought other people could use it too, so the filter works with **your own word lists**. You decide what is important.

---

## What it does (short version)

1. Reads my latest 20 emails from Gmail
2. Skips the ones it already checked before
3. Checks each email with my rules
4. If there are important ones, it sends me **one** email with a list of them

---

## How it works (my notes)

```
Gmail ──► gmail_client.py ──► filters.py ──► seen_store.py ──► notifier.py ──► summary email
          (read emails)       (my rules)     (no repeats)       (send email)
```

`main.py` is like the "boss" file. It doesn't do much by itself, it just calls the other files in the right order.

### `gmail_client.py` – logging in and reading emails
- The first time I run it, a browser opens and Google asks for permission. This is called **OAuth**. My program never sees my Gmail password, Google just gives it a **token**.
- The token is saved in `token.json`, so next time I don't need to log in again. If the token expires, it refreshes it by itself.
- **Scopes** = what permission I ask for. I only ask for two: read emails (`gmail.readonly`) and send emails (`gmail.send`). I didn't ask for delete or edit, because the program doesn't need them.
- `build("gmail", "v1")` gives me a ready "remote control" to talk to the Gmail API.
- For each email I only take the **subject**, **sender** and **snippet** (the short preview), not the whole email. It's faster.

### `filters.py` – deciding if an email is important
My rules are checked in this order:
1. Does it have a **topic word**? (for example "internship", "developer") → if not, ignore it
2. Does it have a **blocked word**? (for example "full-time", "unpaid", "senior") → if yes, ignore it
3. Does it have a **wanted word**? (for example "part-time", "student") → if yes, it's a match ✅

- I join the subject and snippet and make everything **lowercase** first, so "Part-Time" and "part-time" are the same.
- `any(word in text for word in words)` means: is **at least one** of these words in the text?
- The function returns two things: the decision (True/False) **and the reason**, so I can see why an email was accepted or rejected. This helped a lot when testing.

### `preferences.json` + `setup_preferences.py` – your own rules
- The word lists are not inside the code, they are in a JSON file. So anyone can change them without touching Python.
- `setup_preferences.py` asks you questions in the terminal and writes the file for you.

### `seen_store.py` – no duplicate notifications
- Every email has a unique ID. After checking an email I save its ID in `seen_ids.json`.
- I used a **set** because checking "is this ID inside?" is very fast with sets and there are no duplicates.
- So if I run the program 10 times, I still get only one notification for the same email. (I learned this is called **idempotency**.)

### `notifier.py` – sending the summary email
- Uses the same Gmail login, so no extra account or password.
- It asks Gmail "whose account is this?" (`getProfile`) and sends the email to that address, so it works for anyone who uses it.
- Gmail API wants the email in **base64** format, so I convert it before sending.

### `main.py` – putting everything together
- Alert emails start with `[mail-alert]`. The program skips them, otherwise it could read its own notification and send another one forever (infinite loop 😅).
- It saves the seen IDs **at the very end**. If sending fails, the IDs are not saved, so those emails are tried again next time and nothing is lost.

---

## How to run it

1. Create a virtual environment and install the libraries:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
2. In **Google Cloud Console**: create a project → enable **Gmail API** → set up the OAuth consent screen (add yourself as a test user) → create a **Desktop app** OAuth client → download it and rename it to `credentials.json`, put it in the project folder.
3. Set your rules:
   ```
   python setup_preferences.py
   ```
4. Run:
   ```
   python main.py
   ```

⚠️ `credentials.json`, `token.json` and `seen_ids.json` are in `.gitignore`. They are private, so they are never uploaded to GitHub.

---

## Problems I had (and what I learned)

- **WhatsApp didn't work for free.** My first plan was WhatsApp notifications with Twilio. It kept failing with `ContentSid Required` (error 21654). I found out WhatsApp only allows pre-approved message templates, and Twilio's trial account doesn't let you create them. Other WhatsApp options were paid, needed a Facebook business account, or were unofficial libraries that can get your number banned. So I switched to email: it uses the Gmail connection I already had, it's free and reliable. Because the sending code is in its own file (`notifier.py`), changing it didn't break anything else. That was a good lesson about keeping parts separate.
- **Small typos break APIs.** I wrote `userID` instead of `userId` and `max_results` instead of `maxResults`, and the API didn't accept them. API parameter names must be exact.
- **Secrets.** I learned to keep tokens and keys in ignored files and never show them in screenshots.

---

## What I want to add next

- [ ] Better word matching: right now "intern" also matches "international". I want to match whole words only.
- [ ] Run it automatically every hour (Windows Task Scheduler).
- [ ] Unit tests with `pytest` for `filters.py` and `seen_store.py`.
- [ ] Maybe use AI to decide if an email is important, instead of only word lists.
