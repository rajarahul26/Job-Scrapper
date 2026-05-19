# LinkedIn Auto-Apply Design
**Date:** 2026-05-18  
**Status:** Approved

---

## Overview

Add an auto-apply layer on top of the existing cybersecurity job scraper. A new standalone script (`apply.py`) reads the latest scraped Excel output, filters for remote-only jobs, and uses Playwright to auto-apply via LinkedIn Easy Apply. Jobs without Easy Apply have their external URLs opened as browser tabs for manual handling. The existing scraper, GitHub Actions workflow, and config are untouched.

---

## Scope

**In scope:**
- Filter scraped jobs to remote-only
- LinkedIn login with persistent session cookies
- LinkedIn Easy Apply: upload resume, fill screening questions, submit
- Non-Easy-Apply jobs: open external apply URL in a new browser tab
- Track applied jobs to prevent duplicate applications
- Convert `.docx` resume to PDF at runtime for upload (original file untouched)

**Out of scope:**
- Filling out external company application forms
- GitHub Actions integration (runs locally only)
- Modifying `scraper.py`, `config.py`, or `.github/workflows/`

---

## New Files

| File | Purpose |
|------|---------|
| `apply.py` | Main auto-apply script |
| `apply_config.py` | LinkedIn credentials, resume path, screening answers |
| `results/applied_jobs.json` | Tracks already-applied job URLs (auto-created) |
| `linkedin_session.json` | Saved browser cookies (auto-created after first login) |

---

## Remote Filtering Logic

A job is included only if its `Location` field (from the Excel):
- Contains "Remote" (case-insensitive), OR
- Is blank/empty (JobSpy sometimes omits location for fully remote roles)

A job is excluded if location contains a specific city/state that is NOT "Kansas City" or "Overland Park" — those are in-person at the team's own office and not desired.

---

## Resume Handling

- Source: `/Users/rahulkumar/Downloads/Resume_Ehtisham-Mushtaq.docx`
- At runtime, `docx2pdf` converts the `.docx` to a temp PDF in the system temp directory
- The temp PDF is uploaded to LinkedIn Easy Apply, then deleted after the session
- The original `.docx` is never modified, moved, or read for content

---

## LinkedIn Login & Session

1. Bot loads `linkedin_session.json` if it exists
2. Navigates to LinkedIn — if already logged in, proceeds
3. If not logged in (session expired or first run): fills email + password from `apply_config.py`, submits login form
4. After successful login, saves fresh cookies to `linkedin_session.json`
5. Credentials stored only in `apply_config.py` (local file, never committed)

**Note:** `linkedin_session.json` and `apply_config.py` must be added to `.gitignore`.

---

## Easy Apply Flow

For each remote job not in `applied_jobs.json`:

1. Navigate to the LinkedIn job URL
2. Look for the "Easy Apply" button
   - **Found:** proceed with Easy Apply automation (see below)
   - **Not found:** open the job's external apply URL in a new browser tab, log as "manual needed"
3. After successful Easy Apply submission: append job URL to `applied_jobs.json`

### Easy Apply Steps

The Easy Apply modal is multi-step. The bot handles each step:

1. **Contact info step** — fields pre-filled by LinkedIn from profile; bot clicks Next
2. **Resume step** — uploads the temp PDF resume; clicks Next
3. **Screening questions step** — for each question field:
   - Matches question text against known keywords (experience, sponsorship, authorization, phone, city, state)
   - Fills from `SCREENING_ANSWERS` in `apply_config.py`
   - For radio buttons / dropdowns: selects the matching option
   - For unrecognized numeric fields: defaults to `years_of_experience` value
4. **Review step** — clicks Submit
5. **Confirmation** — detects success modal, logs applied

If any step throws an unexpected error, the job is skipped and logged as "failed" (not added to `applied_jobs.json` so it can be retried).

---

## apply_config.py

```python
LINKEDIN_EMAIL    = "ehtishammushtaq@gmail.com"
LINKEDIN_PASSWORD = "Jk13b45512304@@//----"
RESUME_DOCX_PATH  = "/Users/rahulkumar/Downloads/Resume_Ehtisham-Mushtaq.docx"

SCREENING_ANSWERS = {
    "years_of_experience": "5",
    "authorized_to_work_in_us": "Yes",
    "require_sponsorship": "No",
    "phone": "",          # fill in before first run
    "city": "Overland Park",
    "state": "Kansas",
}
```

---

## Duplicate Prevention

`results/applied_jobs.json` is a JSON list of job URLs:

```json
["https://www.linkedin.com/jobs/view/123456", "..."]
```

Before attempting to apply, the bot checks if the job URL is in this list. If yes, skip. This file persists across runs.

---

## Run Instructions

```bash
# 1. Install new dependencies
pip install playwright docx2pdf
playwright install chromium

# 2. Run the scraper first (or wait for Monday's GitHub Actions run)
python scraper.py

# 3. Run the auto-applier
python apply.py
```

The browser opens visibly. You can watch it work. Browser tabs for non-Easy-Apply jobs stay open for you to handle.

---

## End-of-Run Summary

After all jobs are processed, the bot prints:

```
✅ Applied (Easy Apply):     12
🌐 Opened for manual apply:  4
⏭  Already applied (skipped): 3
❌ Failed / skipped:          1
```

---

## Dependencies to Add to requirements.txt

```
playwright
docx2pdf
```

---

## .gitignore Additions

```
apply_config.py
linkedin_session.json
```
