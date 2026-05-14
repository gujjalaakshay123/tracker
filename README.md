# Job Application Tracker

A Python script that reads your Gmail, classifies job-related emails using Claude, and prints a daily report of your job search activity.

## What it does

- Reads emails from the last 24 hours via Gmail API
- Classifies each email into: `application_confirmation`, `rejection`, `interview_invite`, `assessment_request`, `recruiter_outreach`, `follow_up_needed`, or `not_job_related`
- Extracts company name and role title
- Deduplicates (same company + role = one entry)
- Persists history to `history.csv` (skips already-seen emails on future runs)
- Prints a terminal summary: today / week / month counts, status breakdown, ACTION NEEDED items
- Saves a dated markdown report to `logs/`

## Setup

### 1. Google Cloud — Gmail API credentials

You need to do this part in the browser:

1. Go to [Google Cloud Console](https://console.cloud.google.com/) and sign in with your Gmail account.
2. Click the project dropdown at the top → **New Project** → name it (e.g. `job-tracker`) → **Create**.
3. In the left sidebar: **APIs & Services → Library**.
4. Search for **Gmail API** → click it → **Enable**.
5. In the left sidebar: **APIs & Services → OAuth consent screen**.
   - Choose **External** → **Create**.
   - Fill in App name (e.g. `Job Tracker`), your email for support, and your email again for developer contact.
   - Click **Save and Continue** through Scopes (no changes needed) and Test Users.
   - On Test Users: add your own Gmail address → **Save and Continue**.
6. In the left sidebar: **APIs & Services → Credentials**.
   - Click **+ Create Credentials → OAuth client ID**.
   - Application type: **Desktop app** → name it anything → **Create**.
   - Click **Download JSON** on the confirmation dialog (or the download icon on the credentials list).
   - Rename the downloaded file to `credentials.json` and drop it into this project folder.

### 2. Anthropic API key

Get your key from [console.anthropic.com](https://console.anthropic.com/).

```bash
cp .env.example .env
# Edit .env and paste your key:
# ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Install dependencies

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. First run

```bash
source venv/bin/activate
python tracker.py
```

The first run opens a browser window for Gmail OAuth — sign in and grant access. A `token.json` file is saved locally so you won't be prompted again.

## Running daily

Just run:
```bash
cd /path/to/tracker
source venv/bin/activate
python tracker.py
```

## Files

| File | Purpose |
|------|---------|
| `tracker.py` | Main script |
| `credentials.json` | Gmail OAuth client secret (you provide, never commit) |
| `token.json` | Gmail OAuth token (auto-generated, never commit) |
| `history.csv` | Persistent log of all processed emails |
| `logs/YYYY-MM-DD.md` | Daily markdown reports |
| `.env` | Your `ANTHROPIC_API_KEY` (never commit) |
