# Cybersecurity Job Scraper — Session Notes
> Created: 2026-06-24 | Continue from here in next chat

---

## What We Built

A fully automated weekly job scraper that:
- Scrapes **remote contract** cybersecurity jobs from LinkedIn, Indeed (+ Dice attempted)
- Filters strictly by job title keywords (no irrelevant roles)
- Deduplicates across boards
- Saves results as a **formatted Excel (.xlsx)** file with clickable **Apply Now** links
- **Emails the Excel** to `rajrahul1326@gmail.com` every Monday at 8am UTC automatically
- Runs free on **GitHub Actions** — no server, no cost

---

## GitHub Repo

- **URL:** https://github.com/rajarahul26/Job-Scrapper
  *(Note: repo was renamed/moved from `rajrahul1326-commits` to `rajarahul26` during session)*
- **Branch:** `main`
- **Local clone:** `~/Job-Scrapper`

---

## File Structure

```
Job-Scrapper/
├── config.py                          ← EDIT THIS to change roles, filters, boards
├── scraper.py                         ← Main scraper logic (do not edit unless needed)
├── requirements.txt                   ← Python dependencies
├── .github/
│   └── workflows/
│       └── job-scraper.yml            ← GitHub Actions schedule (every Monday 8am UTC)
└── results/
    └── cybersecurity-jobs-YYYY-MM-DD.xlsx   ← Weekly output saved here
```

---

## Current Config (config.py)

```python
JOB_ROLES = [
    "IAM Engineer",
    "PAM Engineer",
    "CyberArk Engineer",
    "Cloud Security Engineer",
    "Cybersecurity Consultant",
    "Security Architect",
    "Incident Response Engineer",
    "Penetration Tester",
]

LOCATIONS = ["United States"]
DAYS_BACK = 7
JOB_TYPE = "contract"       # contract only
REMOTE_ONLY = True          # remote only

SCRAPE_LINKEDIN = True
SCRAPE_INDEED = True
SCRAPE_GLASSDOOR = False    # blocked GitHub IPs
SCRAPE_DICE = True          # configured but returns 0 — see Known Issues
SCRAPE_ZIPRECRUITER = False
SCRAPE_GOOGLE = False

EMAIL_RECIPIENT = "rajrahul1326@gmail.com"
```

---

## GitHub Secrets (already configured)

| Secret | Purpose |
|--------|---------|
| `EMAIL_SENDER` | Gmail address that sends the email |
| `EMAIL_PASSWORD` | Gmail App Password (16-char) |
| `EMAIL_RECIPIENT` | rajrahul1326@gmail.com |

Settings at: https://github.com/rajarahul26/Job-Scrapper/settings/secrets/actions

---

## How to Trigger a Manual Run

```bash
cd ~/Job-Scrapper
gh workflow run job-scraper.yml
```

Or via GitHub UI:
**Actions tab → Weekly Cybersecurity Job Scraper → Run workflow**

---

## How to Push Changes

```bash
cd ~/Job-Scrapper
git add config.py          # or whichever file you changed
git commit -m "Your message"
git pull origin main --rebase
git push origin main
```

---

## Last Run Results (2026-06-24)

- **119 unique remote contract jobs** found
- Sources: LinkedIn + Indeed
- Excel emailed successfully to rajrahul1326@gmail.com
- Results saved: `results/cybersecurity-jobs-2026-06-24.xlsx`

---

## Known Issues / What's Left

### 1. Dice.com — Returns 0 Results
- **Problem:** Dice blocks GitHub Actions cloud IPs (403 on API, 0 results on RSS fallback)
- **Options to fix:**
  - Try ZipRecruiter instead (`SCRAPE_ZIPRECRUITER = True` — test with contract/remote params)
  - Use a residential proxy service (adds cost)
  - Leave as-is — LinkedIn + Indeed cover most Dice postings anyway
- **Status:** Pending decision

### 2. Glassdoor — Disabled
- Consistently returns API errors from GitHub cloud IPs
- Left disabled (`SCRAPE_GLASSDOOR = False`)

### 3. Node.js 20 Deprecation Warning
- GitHub Actions warns that `actions/checkout@v4` and `actions/setup-python@v4` use Node 20
- Not breaking anything yet, but should update workflow before September 2026
- Fix: bump to `actions/checkout@v5` and `actions/setup-python@v5` in `.github/workflows/job-scraper.yml`

---

## Quick Edit Guide

### Add a job role:
Edit `config.py` → add to `JOB_ROLES` list → push

### Switch back to all job types (not just contract):
```python
JOB_TYPE = None   # or "fulltime"
REMOTE_ONLY = False
```

### Add ZipRecruiter (to replace Dice):
```python
SCRAPE_ZIPRECRUITER = True
```

### Change schedule (currently Monday 8am UTC):
Edit `.github/workflows/job-scraper.yml`:
```yaml
- cron: '0 8 * * 1'   # minute hour * * day-of-week (1=Monday)
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Job scraping | `python-jobspy` 1.1.82 |
| Excel output | `openpyxl` |
| Email | Gmail SMTP (port 587 + TLS) |
| Automation | GitHub Actions (cron) |
| Language | Python 3.11 |
| Hosting | GitHub (free) |

---

## Commands Reference

```bash
# Trigger manual run
gh workflow run job-scraper.yml

# Watch live run
gh run list --limit 1
gh run watch <RUN_ID>

# Check run logs
gh run view <RUN_ID> --log

# Push changes
git add . && git commit -m "message" && git pull origin main --rebase && git push origin main
```
