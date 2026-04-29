# 🔍 Cybersecurity Job Scraper

Automatically scrape and email **cybersecurity job listings** (IAM, PAM, CyberArk, Security Engineer roles) from **LinkedIn, Indeed, Glassdoor, ZipRecruiter, and Google Jobs** every week.

**Built with:** JobSpy + GitHub Actions + Python  
**Cost:** 100% Free  
**Update Frequency:** Weekly (configurable)

---

## ⚡ Quick Start

### Step 1: Create a GitHub Repository

1. Go to **github.com** (login/create account if needed)
2. Click **"+"** (top right) → **"New repository"**
3. Name it: `cybersecurity-job-scraper`
4. Choose **Public** (easier) or **Private**
5. ✅ Click **"Create repository"**

### Step 2: Download These Files to Your Computer

Create these files locally:

```
cybersecurity-job-scraper/
├── config.py
├── scraper.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── job-scraper.yml
└── README.md (this file)
```

**Copy the contents from:**
- `config.py` → [use the provided config.py]
- `scraper.py` → [use the provided scraper.py]
- `requirements.txt` → [use the provided requirements.txt]
- `.github/workflows/job-scraper.yml` → [create folder & use the workflow file]

### Step 3: Push to GitHub

```bash
# Clone your repo to your computer
git clone https://github.com/YOUR_USERNAME/cybersecurity-job-scraper.git
cd cybersecurity-job-scraper

# Copy the 4 files above into this folder

# Add, commit, and push
git add .
git commit -m "Initial job scraper setup"
git push origin main
```

### Step 4: Set Up Gmail App Password

GitHub Actions needs your Gmail credentials to send emails. **Important:** Use an **App Password**, NOT your regular Gmail password.

#### Create a Gmail App Password:

1. Go to **myaccount.google.com** → **Security** (left menu)
2. Enable **2-Step Verification** if not already done
3. Scroll down → Click **"App passwords"**
4. Select **Mail** + **Windows Computer** (doesn't matter)
5. Copy the **16-character password** shown
6. Save it somewhere safe — you'll need it in the next step

### Step 5: Add GitHub Secrets

GitHub Secrets store your email credentials safely (encrypted).

1. Go to your GitHub repo → **Settings** (top right)
2. Click **"Secrets and variables"** → **"Actions"** (left menu)
3. Click **"New repository secret"**

**Add 3 secrets:**

| Secret Name | Value | Example |
|-------------|-------|---------|
| `EMAIL_SENDER` | Your Gmail address | `rajrahul1326@gmail.com` |
| `EMAIL_PASSWORD` | Your 16-char App Password | `abcd efgh ijkl mnop` |
| `EMAIL_RECIPIENT` | Where to send results | `rajrahul1326@gmail.com` |

**How to add:**
1. Name: `EMAIL_SENDER`
2. Value: `rajrahul1326@gmail.com`
3. Click **"Add secret"**
4. Repeat for `EMAIL_PASSWORD` and `EMAIL_RECIPIENT`

---

## 🎯 Customizing Your Scraper

### Edit Job Roles

Open `config.py` in your GitHub repo and edit:

```python
JOB_ROLES = [
    "IAM Engineer",          # Keep these
    "PAM Engineer",
    "CyberArk Engineer",
    "Cloud Security Engineer",  # Add/remove as needed
    "Incident Response Engineer",
    # Add more roles here
]
```

**To add a role:**
```python
JOB_ROLES = [
    "Security Architect",  # Add this
    # ... rest of list
]
```

**Then:**
1. Commit the change: `git add config.py && git commit -m "Add Security Architect role"`
2. Push: `git push`

### Change Email Recipient

Edit in `config.py`:

```python
EMAIL_RECIPIENT = "newemail@example.com"
```

### Adjust How Many Days Back

```python
DAYS_BACK = 14  # Change from 7 to 14 for 2 weeks
```

### Change Which Job Boards to Search

```python
SCRAPE_LINKEDIN = True      # LinkedIn
SCRAPE_INDEED = True        # Indeed
SCRAPE_GLASSDOOR = True     # Glassdoor
SCRAPE_ZIPRECRUITER = True  # ZipRecruiter
SCRAPE_GOOGLE = True        # Google Jobs
```

Set any to `False` to skip that source.

### Change How Many Results Per Role

```python
RESULTS_PER_ROLE = 50  # Change from 30 (max ~50)
```

---

## 🚀 Running the Scraper

### Automatic (Weekly)

The scraper runs **every Monday at 8:00 AM UTC** automatically.

To **change the schedule**, edit `.github/workflows/job-scraper.yml`:

```yaml
on:
  schedule:
    - cron: '0 8 * * 1'  # Monday 8 AM UTC
```

**Cron format:** `minute hour day-of-week`
- `0 8 * * 1` = Every Monday, 8 AM
- `0 9 * * *` = Every day, 9 AM
- `30 14 * * 1-5` = Weekdays, 2:30 PM

### Manual Run (Anytime)

1. Go to **GitHub repo** → **Actions** tab
2. Click **"Weekly Cybersecurity Job Scraper"** (left sidebar)
3. Click **"Run workflow"** → **"Run workflow"** (green button)
4. Wait ~2 min → Results emailed to you + saved to `results/` folder

---

## 📊 Viewing Results

### In Your Email

Every Monday (or after manual run), you'll get an email with:
- 📈 Job count by role
- 🔗 Job count by source (LinkedIn, Indeed, etc.)
- 📥 CSV attachment with full details

### In Your GitHub Repo

Results saved to `results/cybersecurity-jobs-YYYY-MM-DD.csv`

1. Go to **GitHub repo** → **results** folder
2. Click any CSV file
3. See job title, company, location, salary, job URL, etc.

---

## 🔧 Troubleshooting

### Email Not Received

**Problem:** You get an error about email credentials.

**Solution:**
1. Verify your **Email App Password** is correct (16 characters, from Step 4 above)
2. Check **GitHub Secrets** are set correctly (Settings → Secrets → Actions)
3. Make sure 2-Step Verification is enabled on your Gmail account

### No Jobs Found

**Problem:** Scraper runs but finds 0 jobs.

**Solution:**
1. Job board might be down or rate-limiting
2. Try adding more `RESULTS_PER_ROLE` in config.py
3. Check if job title spelling is correct
4. Try disabling some job boards (e.g., set `SCRAPE_LINKEDIN = False`)

### Scraper Errors in GitHub Actions

**To see detailed logs:**
1. Go to **GitHub repo** → **Actions** tab
2. Click the **failed run**
3. Click **"scrape"** job → **"Run job scraper"** step
4. See error message

---

## 📝 Example: Adding a New Job Role

Let's say you want to add "Security Operations Manager":

1. **Edit `config.py`:**
   ```python
   JOB_ROLES = [
       "IAM Engineer",
       "PAM Engineer",
       "Security Operations Manager",  # Add this line
   ]
   ```

2. **Commit and push:**
   ```bash
   git add config.py
   git commit -m "Add Security Operations Manager role"
   git push
   ```

3. **Next Monday (or manual trigger)**, the scraper will search for this role too!

---

## 📧 Gmail App Password Help

**Why use App Password instead of regular password?**
- GitHub Secrets can't access your regular Gmail password (for security)
- App Passwords are temporary codes that work only with apps
- Easier to disable if compromised

**If you don't see "App passwords" option:**
1. Make sure **2-Step Verification** is ON (required)
2. Retry the steps in Step 4 above

---

## 🎯 Expected Workflow

```
Every Monday 8 AM (UTC)
    ↓
GitHub Actions triggers scraper
    ↓
Scraper searches 8 job roles across 5 job boards
    ↓
Filters results: last 7 days only
    ↓
Saves CSV to results/ folder
    ↓
Commits to GitHub repo
    ↓
Sends email to rajrahul1326@gmail.com with summary
    ↓
✅ Done! Review jobs in email or CSV
```

---

## 💡 Tips

- **Test locally first:** `python scraper.py` (after `pip install -r requirements.txt`)
- **Backup your secrets:** Save your Gmail App Password somewhere safe
- **Adjust roles monthly:** Add/remove roles as your job search evolves
- **Check email junk folder:** GitHub emails sometimes get filtered
- **Scale up:** Add more job titles/locations to search more broadly

---

## 🚀 Future Enhancements

You can later add:
- Slack/Discord notifications
- Salary filtering
- Keywords filtering (e.g., remote-only)
- Job description summaries with AI
- Database storage instead of CSV

---

## 📞 Support

If you get stuck:
1. Check **Troubleshooting** section above
2. Check GitHub Actions **logs** (Actions tab → failed run)
3. Verify Gmail **App Password** is correct
4. Make sure GitHub **Secrets** are set

---

**Happy job hunting! 🎯**
