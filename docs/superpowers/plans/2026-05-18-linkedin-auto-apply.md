# LinkedIn Auto-Apply Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local Playwright script (`apply.py`) that reads the latest scraped Excel, filters remote-only jobs, auto-applies via LinkedIn Easy Apply, and opens browser tabs for non-Easy-Apply jobs.

**Architecture:** `apply_config.py` holds all credentials and screening answers. `apply.py` contains all logic as focused functions — Excel reading, remote filtering, applied-job tracking, resume conversion, LinkedIn login, Easy Apply modal handling, and main orchestration. A JSON file in `results/` persists which URLs have already been applied to across runs.

**Tech Stack:** Python 3, Playwright (sync API), openpyxl, docx2pdf, json, glob, tempfile

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `apply_config.py` | Create | Credentials, resume path, screening answers |
| `apply.py` | Create | All auto-apply logic |
| `tests/test_apply.py` | Create | Unit tests for filter + tracker + Excel reader |
| `requirements.txt` | Modify | Add `playwright`, `docx2pdf` |
| `.gitignore` | Modify | Exclude `apply_config.py`, `linkedin_session.json` |
| `results/applied_jobs.json` | Auto-created at runtime | Tracks applied job URLs |
| `linkedin_session.json` | Auto-created at runtime | Saved browser cookies |

---

## Task 1: Update requirements.txt and .gitignore

**Files:**
- Modify: `requirements.txt`
- Modify: `.gitignore` (create if missing)

- [ ] **Step 1: Add new dependencies to requirements.txt**

Open `requirements.txt` and replace its contents with:

```
python-jobspy
pandas>=2.0.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
openpyxl>=3.1.0
playwright
docx2pdf
pytest
```

- [ ] **Step 2: Create/update .gitignore**

Create `.gitignore` in the project root (or append if it exists):

```
apply_config.py
linkedin_session.json
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 3: Install dependencies**

```bash
pip install playwright docx2pdf pytest
playwright install chromium
```

Expected output ends with: `✔ Chromium ... Downloading` and then `✔ Download complete`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt .gitignore
git commit -m "feat: add playwright, docx2pdf, pytest deps"
```

---

## Task 2: Create apply_config.py

**Files:**
- Create: `apply_config.py`

- [ ] **Step 1: Create the config file**

```python
LINKEDIN_EMAIL    = "ehtishammushtaq@gmail.com"
LINKEDIN_PASSWORD = "Jk13b45512304@@//----"
RESUME_DOCX_PATH  = "/Users/rahulkumar/Downloads/Resume_Ehtisham-Mushtaq.docx"

SCREENING_ANSWERS = {
    "years_of_experience": "5",
    "authorized_to_work_in_us": "Yes",
    "require_sponsorship": "No",
    "phone": "",        # fill in Ehtisham's phone before first run
    "city": "Overland Park",
    "state": "Kansas",
}
```

- [ ] **Step 2: Verify the file is gitignored**

```bash
git check-ignore -v apply_config.py
```

Expected output: `.gitignore:1:apply_config.py    apply_config.py`

---

## Task 3: Write failing tests for remote filter and applied-job tracker

**Files:**
- Create: `tests/__init__.py` (empty)
- Create: `tests/test_apply.py`

- [ ] **Step 1: Create tests directory and empty init**

```bash
mkdir -p tests && touch tests/__init__.py
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_apply.py`:

```python
import json
import os
import pytest
from apply import (
    is_remote_job,
    load_applied_jobs,
    save_applied_job,
    get_latest_excel,
)


# --- is_remote_job ---

def test_remote_keyword():
    assert is_remote_job({"Location": "Remote"}) is True

def test_remote_case_insensitive():
    assert is_remote_job({"Location": "remote"}) is True
    assert is_remote_job({"Location": "REMOTE"}) is True

def test_remote_in_phrase():
    assert is_remote_job({"Location": "United States (Remote)"}) is True

def test_blank_location_is_remote():
    assert is_remote_job({"Location": ""}) is True

def test_missing_location_key_is_remote():
    assert is_remote_job({}) is True

def test_specific_city_not_remote():
    assert is_remote_job({"Location": "New York, NY"}) is False

def test_austin_not_remote():
    assert is_remote_job({"Location": "Austin, TX"}) is False

def test_kansas_city_not_remote():
    assert is_remote_job({"Location": "Kansas City, MO"}) is False


# --- load_applied_jobs / save_applied_job ---

def test_load_empty_when_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    assert load_applied_jobs() == set()

def test_save_and_reload(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    applied = load_applied_jobs()
    applied = save_applied_job("https://www.linkedin.com/jobs/view/123", applied)
    reloaded = load_applied_jobs()
    assert "https://www.linkedin.com/jobs/view/123" in reloaded

def test_no_duplicate_saved(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    applied = load_applied_jobs()
    applied = save_applied_job("https://www.linkedin.com/jobs/view/999", applied)
    applied = save_applied_job("https://www.linkedin.com/jobs/view/999", applied)
    reloaded = load_applied_jobs()
    assert list(reloaded).count("https://www.linkedin.com/jobs/view/999") == 1

def test_multiple_jobs_saved(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    applied = load_applied_jobs()
    applied = save_applied_job("https://www.linkedin.com/jobs/view/1", applied)
    applied = save_applied_job("https://www.linkedin.com/jobs/view/2", applied)
    reloaded = load_applied_jobs()
    assert len(reloaded) == 2


# --- get_latest_excel ---

def test_get_latest_excel_returns_most_recent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    older = tmp_path / "results" / "jobs-2026-05-01.xlsx"
    newer = tmp_path / "results" / "jobs-2026-05-18.xlsx"
    older.write_bytes(b"x")
    import time; time.sleep(0.01)
    newer.write_bytes(b"x")
    assert get_latest_excel().endswith("jobs-2026-05-18.xlsx")

def test_get_latest_excel_raises_when_empty(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("results")
    with pytest.raises(FileNotFoundError):
        get_latest_excel()
```

- [ ] **Step 3: Run tests — verify they all fail**

```bash
pytest tests/test_apply.py -v
```

Expected: all tests fail with `ModuleNotFoundError: No module named 'apply'`

---

## Task 4: Implement remote filter, applied tracker, and Excel finder in apply.py

**Files:**
- Create: `apply.py`

- [ ] **Step 1: Create apply.py with the three functions under test**

```python
#!/usr/bin/env python3
import glob
import json
import os
import tempfile
from typing import Dict, List, Set

import openpyxl
from playwright.sync_api import sync_playwright

from apply_config import (
    LINKEDIN_EMAIL,
    LINKEDIN_PASSWORD,
    RESUME_DOCX_PATH,
    SCREENING_ANSWERS,
)

APPLIED_FILE  = "results/applied_jobs.json"
SESSION_FILE  = "linkedin_session.json"
EXCEL_COLUMNS = [
    "Job Title", "Company", "Location", "Job Type",
    "Salary Min", "Salary Max", "Currency", "Date Posted",
    "Source", "Apply Link",
]


# ---------------------------------------------------------------------------
# Excel helpers
# ---------------------------------------------------------------------------

def get_latest_excel() -> str:
    files = glob.glob("results/*.xlsx")
    if not files:
        raise FileNotFoundError("No Excel files found in results/")
    return max(files, key=os.path.getmtime)


def read_jobs_from_excel(path: str) -> List[Dict]:
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    jobs = []
    for row in ws.iter_rows(min_row=2, values_only=False):
        job = {}
        for i, cell in enumerate(row):
            col_name = EXCEL_COLUMNS[i] if i < len(EXCEL_COLUMNS) else f"col_{i}"
            if col_name == "Apply Link":
                job["job_url"] = cell.hyperlink.target if cell.hyperlink else ""
            else:
                job[col_name] = cell.value or ""
        jobs.append(job)
    return jobs


# ---------------------------------------------------------------------------
# Remote filter
# ---------------------------------------------------------------------------

def is_remote_job(job: Dict) -> bool:
    location = str(job.get("Location", "")).strip().lower()
    if not location:
        return True
    return "remote" in location


# ---------------------------------------------------------------------------
# Applied-job tracker
# ---------------------------------------------------------------------------

def load_applied_jobs() -> Set[str]:
    if not os.path.exists(APPLIED_FILE):
        return set()
    with open(APPLIED_FILE) as f:
        return set(json.load(f))


def save_applied_job(url: str, applied: Set[str]) -> Set[str]:
    applied.add(url)
    with open(APPLIED_FILE, "w") as f:
        json.dump(list(applied), f, indent=2)
    return applied
```

- [ ] **Step 2: Run tests — verify they all pass**

```bash
pytest tests/test_apply.py -v
```

Expected: all 14 tests pass, 0 failures.

- [ ] **Step 3: Commit**

```bash
git add apply.py tests/
git commit -m "feat: remote filter, applied tracker, excel finder with tests"
```

---

## Task 5: Resume conversion

**Files:**
- Modify: `apply.py` — add `convert_resume_to_pdf()`
- Modify: `tests/test_apply.py` — add conversion test

- [ ] **Step 1: Add the failing test to tests/test_apply.py**

Append to `tests/test_apply.py`:

```python
# --- convert_resume_to_pdf ---

def test_convert_resume_creates_pdf():
    from apply import convert_resume_to_pdf
    from apply_config import RESUME_DOCX_PATH
    if not os.path.exists(RESUME_DOCX_PATH):
        pytest.skip("Resume file not present on this machine")
    pdf_path = convert_resume_to_pdf()
    try:
        assert os.path.exists(pdf_path)
        assert pdf_path.endswith(".pdf")
        assert os.path.getsize(pdf_path) > 0
    finally:
        os.unlink(pdf_path)
```

- [ ] **Step 2: Run test — verify it fails**

```bash
pytest tests/test_apply.py::test_convert_resume_creates_pdf -v
```

Expected: FAIL with `ImportError: cannot import name 'convert_resume_to_pdf'`

- [ ] **Step 3: Implement convert_resume_to_pdf in apply.py**

Add after the `save_applied_job` function:

```python
# ---------------------------------------------------------------------------
# Resume conversion
# ---------------------------------------------------------------------------

def convert_resume_to_pdf() -> str:
    from docx2pdf import convert
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    tmp.close()
    convert(RESUME_DOCX_PATH, tmp.name)
    return tmp.name
```

- [ ] **Step 4: Run test — verify it passes**

```bash
pytest tests/test_apply.py::test_convert_resume_creates_pdf -v
```

Expected: PASS

- [ ] **Step 5: Run full suite to confirm no regressions**

```bash
pytest tests/test_apply.py -v
```

Expected: all 15 tests pass.

- [ ] **Step 6: Commit**

```bash
git add apply.py tests/test_apply.py
git commit -m "feat: docx-to-pdf resume conversion with test"
```

---

## Task 6: LinkedIn session manager

**Files:**
- Modify: `apply.py` — add `linkedin_login()`

*This function drives a real browser — unit tests aren't practical. Manual verification is in Task 10.*

- [ ] **Step 1: Add linkedin_login to apply.py**

Add after `convert_resume_to_pdf`:

```python
# ---------------------------------------------------------------------------
# LinkedIn session
# ---------------------------------------------------------------------------

def linkedin_login(page, context) -> None:
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            context.add_cookies(json.load(f))

    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_load_state("networkidle", timeout=15000)

    if "/feed" in page.url:
        print("✅ LinkedIn: session still valid")
        return

    print("🔐 LinkedIn: logging in...")
    page.goto("https://www.linkedin.com/login")
    page.wait_for_selector("#username", timeout=10000)
    page.fill("#username", LINKEDIN_EMAIL)
    page.fill("#password", LINKEDIN_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_url("**/feed/**", timeout=20000)

    cookies = context.cookies()
    with open(SESSION_FILE, "w") as f:
        json.dump(cookies, f)
    print("✅ LinkedIn: logged in, session saved")
```

- [ ] **Step 2: Commit**

```bash
git add apply.py
git commit -m "feat: LinkedIn session manager with cookie persistence"
```

---

## Task 7: Screening questions handler

**Files:**
- Modify: `apply.py` — add `_match_answer()` and `fill_screening_questions()`

- [ ] **Step 1: Add screening answer matcher test to tests/test_apply.py**

Append to `tests/test_apply.py`:

```python
# --- _match_answer ---

def test_match_years_of_experience():
    from apply import _match_answer
    assert _match_answer("years of experience") == "5"

def test_match_sponsorship():
    from apply import _match_answer
    assert _match_answer("do you require visa sponsorship") == "No"

def test_match_authorized():
    from apply import _match_answer
    assert _match_answer("are you legally authorized to work in the us") == "Yes"

def test_match_phone():
    from apply import _match_answer
    # phone may be empty string — just verify it returns the configured value
    from apply_config import SCREENING_ANSWERS
    from apply import _match_answer
    assert _match_answer("phone number") == SCREENING_ANSWERS["phone"]

def test_match_city():
    from apply import _match_answer
    assert _match_answer("city") == "Overland Park"

def test_match_state():
    from apply import _match_answer
    assert _match_answer("state") == "Kansas"

def test_match_unknown_numeric_defaults_to_years():
    from apply import _match_answer
    assert _match_answer("how many years have you worked in cybersecurity") == "5"
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
pytest tests/test_apply.py -k "match" -v
```

Expected: FAIL with `ImportError: cannot import name '_match_answer'`

- [ ] **Step 3: Implement _match_answer and fill_screening_questions in apply.py**

Add after `linkedin_login`:

```python
# ---------------------------------------------------------------------------
# Screening questions
# ---------------------------------------------------------------------------

def _match_answer(label_lower: str) -> str:
    if any(k in label_lower for k in ["year", "experience"]):
        return SCREENING_ANSWERS["years_of_experience"]
    if any(k in label_lower for k in ["sponsor", "visa"]):
        return SCREENING_ANSWERS["require_sponsorship"]
    if any(k in label_lower for k in ["authorized", "legally", "eligible"]):
        return SCREENING_ANSWERS["authorized_to_work_in_us"]
    if "phone" in label_lower:
        return SCREENING_ANSWERS["phone"]
    if "city" in label_lower:
        return SCREENING_ANSWERS["city"]
    if "state" in label_lower:
        return SCREENING_ANSWERS["state"]
    return SCREENING_ANSWERS["years_of_experience"]


def fill_screening_questions(page) -> None:
    for field in page.locator(".jobs-easy-apply-form-element").all():
        try:
            label = (field.locator("label").first.text_content() or "").lower()

            text_input = field.locator("input[type='text'], input[type='tel'], input[type='number']")
            if text_input.count() > 0 and text_input.first.is_visible():
                value = _match_answer(label)
                if value:
                    text_input.first.clear()
                    text_input.first.fill(value)
                continue

            select = field.locator("select")
            if select.count() > 0 and select.first.is_visible():
                value = _match_answer(label)
                if value:
                    options = select.first.locator("option").all_text_contents()
                    match = next((o for o in options if value.lower() in o.lower()), None)
                    if match:
                        select.first.select_option(label=match)
                continue

            for radio in field.locator("input[type='radio']").all():
                radio_value = (radio.get_attribute("value") or "").lower()
                answer = _match_answer(label).lower()
                if radio_value and radio_value in answer:
                    radio.click()
                    break

        except Exception:
            continue
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
pytest tests/test_apply.py -k "match" -v
```

Expected: all 7 match tests pass.

- [ ] **Step 5: Run full suite**

```bash
pytest tests/test_apply.py -v
```

Expected: all 22 tests pass.

- [ ] **Step 6: Commit**

```bash
git add apply.py tests/test_apply.py
git commit -m "feat: screening questions handler with answer matcher tests"
```

---

## Task 8: Easy Apply modal handler

**Files:**
- Modify: `apply.py` — add `handle_easy_apply()` and `_fill_modal_step()`

- [ ] **Step 1: Add handle_easy_apply and _fill_modal_step to apply.py**

Add after `fill_screening_questions`:

```python
# ---------------------------------------------------------------------------
# Easy Apply modal
# ---------------------------------------------------------------------------

def _fill_modal_step(page, resume_pdf: str) -> None:
    upload = page.locator("input[type='file']")
    if upload.count() > 0 and upload.first.is_visible():
        upload.first.set_input_files(resume_pdf)
        page.wait_for_timeout(2000)

    fill_screening_questions(page)


def handle_easy_apply(page, job: Dict, resume_pdf: str) -> bool:
    page.goto(job["job_url"])
    page.wait_for_load_state("networkidle", timeout=15000)

    easy_btn = page.locator("button.jobs-apply-button").first
    if not easy_btn.is_visible():
        return False

    easy_btn.click()
    page.wait_for_selector(".jobs-easy-apply-modal", timeout=8000)

    max_steps = 10
    for _ in range(max_steps):
        page.wait_for_timeout(800)
        _fill_modal_step(page, resume_pdf)

        submit_btn = page.locator("button[aria-label='Submit application']")
        if submit_btn.is_visible():
            submit_btn.click()
            page.wait_for_timeout(2000)
            dismiss = page.locator("button[aria-label='Dismiss']")
            if dismiss.is_visible():
                dismiss.click()
            return True

        review_btn = page.locator("button[aria-label='Review your application']")
        if review_btn.is_visible():
            review_btn.click()
            continue

        next_btn = page.locator("button[aria-label='Continue to next step']")
        if next_btn.is_visible():
            next_btn.click()
            continue

        break

    return False
```

- [ ] **Step 2: Commit**

```bash
git add apply.py
git commit -m "feat: Easy Apply modal handler with multi-step navigation"
```

---

## Task 9: Main orchestration

**Files:**
- Modify: `apply.py` — add `main()`

- [ ] **Step 1: Add main() to apply.py**

Add at the bottom of `apply.py`:

```python
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("🤖 LINKEDIN AUTO-APPLIER")
    print("=" * 60 + "\n")

    excel_path = get_latest_excel()
    print(f"📂 Reading jobs from: {excel_path}")
    jobs = read_jobs_from_excel(excel_path)

    remote_jobs = [j for j in jobs if is_remote_job(j)]
    print(f"🌐 Remote jobs found: {len(remote_jobs)} / {len(jobs)} total\n")

    applied = load_applied_jobs()
    resume_pdf = convert_resume_to_pdf()
    print(f"📄 Resume converted to temp PDF: {resume_pdf}\n")

    stats = {"easy_apply": 0, "manual": 0, "skipped": 0, "failed": 0}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=500)
            context = browser.new_context()
            page = context.new_page()

            linkedin_login(page, context)

            for job in remote_jobs:
                url = job.get("job_url", "")
                title = job.get("Job Title", "Unknown")
                company = job.get("Company", "")

                if not url:
                    stats["skipped"] += 1
                    continue

                if url in applied:
                    print(f"⏭  Already applied: {title} @ {company}")
                    stats["skipped"] += 1
                    continue

                source = str(job.get("Source", "")).lower()
                print(f"🔍 {title} @ {company} [{source}]")

                try:
                    if source == "linkedin":
                        success = handle_easy_apply(page, job, resume_pdf)
                        if success:
                            applied = save_applied_job(url, applied)
                            print(f"   ✅ Easy Apply submitted")
                            stats["easy_apply"] += 1
                        else:
                            tab = context.new_page()
                            tab.goto(url)
                            print(f"   🌐 Opened for manual apply")
                            stats["manual"] += 1
                    else:
                        tab = context.new_page()
                        tab.goto(url)
                        print(f"   🌐 Opened for manual apply ({source})")
                        stats["manual"] += 1

                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    stats["failed"] += 1

            print(f"\n{'=' * 60}")
            print(f"✅ Applied (Easy Apply):      {stats['easy_apply']}")
            print(f"🌐 Opened for manual apply:   {stats['manual']}")
            print(f"⏭  Already applied (skipped): {stats['skipped']}")
            print(f"❌ Failed / skipped:           {stats['failed']}")
            print(f"{'=' * 60}")

            input("\nPress Enter to close the browser...")
            browser.close()

    finally:
        if os.path.exists(resume_pdf):
            os.unlink(resume_pdf)
            print("🧹 Temp resume PDF deleted")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run full test suite to confirm nothing broke**

```bash
pytest tests/test_apply.py -v
```

Expected: all 22 tests pass.

- [ ] **Step 3: Commit**

```bash
git add apply.py
git commit -m "feat: main orchestration — remote filter, Easy Apply, tab opener, summary"
```

---

## Task 10: End-to-end smoke test (manual)

*Playwright drives a real browser — automated tests aren't practical here. Run manually.*

- [ ] **Step 1: Fill in phone number in apply_config.py**

Open `apply_config.py` and set:

```python
"phone": "913XXXXXXX",  # replace with Ehtisham's actual phone
```

- [ ] **Step 2: Run the applier against the latest Excel**

```bash
python apply.py
```

Expected behaviour:
- Chromium browser opens visibly
- LinkedIn login page appears briefly, then redirects to feed (or skips if cookies valid)
- Console prints remote job count
- For each remote LinkedIn job: Easy Apply modal opens, resume uploads, questions fill, Submit clicked
- For non-LinkedIn or non-Easy-Apply jobs: new browser tabs open
- End-of-run summary prints counts
- Press Enter closes browser, temp PDF deleted

- [ ] **Step 3: Verify applied_jobs.json was created**

```bash
cat results/applied_jobs.json
```

Expected: a JSON array of LinkedIn job URLs that were Easy Applied.

- [ ] **Step 4: Re-run to verify no duplicate applications**

```bash
python apply.py
```

Expected: all previously applied jobs print `⏭  Already applied` and stats show them as skipped.

- [ ] **Step 5: Final commit**

```bash
git add results/applied_jobs.json
git commit -m "chore: add initial applied_jobs tracker (post smoke test)"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ Remote-only filter (Task 4)
- ✅ LinkedIn Easy Apply automation (Tasks 6–8)
- ✅ Non-Easy-Apply: open browser tabs (Task 9)
- ✅ Screening questions pre-filled from config (Task 7)
- ✅ Resume: docx → temp PDF, original untouched (Task 5)
- ✅ Session cookie persistence (Task 6)
- ✅ Duplicate prevention via applied_jobs.json (Tasks 3–4)
- ✅ Existing scraper/workflow untouched (apply.py is standalone)
- ✅ End-of-run summary (Task 9)

**Placeholder scan:** No TBDs. Phone is intentionally blank with a comment to fill before first run.

**Type consistency:** `load_applied_jobs()` returns `Set[str]`, `save_applied_job()` accepts and returns `Set[str]` — consistent across Tasks 3, 4, and 9. `handle_easy_apply()` returns `bool` — used correctly in `main()`.
