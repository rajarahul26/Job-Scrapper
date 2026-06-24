# =============================================================================
# CONFIG.PY - EDIT THIS FILE TO CUSTOMIZE YOUR JOB SCRAPER
# =============================================================================

# Job roles to search for (add or remove as needed)
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

# Locations to search (USA-wide)
LOCATIONS = [
    "United States",
]

# Number of days to look back (default: 7 for last week)
DAYS_BACK = 7

# Email configuration
# These will be set as GitHub Secrets - see README.md for setup
EMAIL_SENDER = "your-email@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "your-app-password"   # Gmail App Password (NOT your regular password)
EMAIL_RECIPIENT = "rajrahul1326@gmail.com"  # Where to send results

# Results output
OUTPUT_DIR = "results"
OUTPUT_FILENAME_PREFIX = "cybersecurity-jobs"  # Files will be named: cybersecurity-jobs-2026-04-29.csv

# Scraper settings
RESULTS_PER_ROLE = 30  # Number of job listings per role (max ~50)

# Email subject line
EMAIL_SUBJECT = "Weekly Cybersecurity Job Scraper Results - IAM/PAM/Security Roles"

# Job type filter — "contract" | "fulltime" | "parttime" | None (None = all types)
JOB_TYPE = "contract"

# Remote only — True = only remote jobs, False = all locations
REMOTE_ONLY = True

# Job boards to scrape
SCRAPE_LINKEDIN = True
SCRAPE_INDEED = True
SCRAPE_GLASSDOOR = True
SCRAPE_DICE = True           # Dice.com — great for contract/IT roles
SCRAPE_ZIPRECRUITER = False  # Disabled - unreliable
SCRAPE_GOOGLE = False        # Disabled - unreliable

# Title filter — job title MUST contain at least one of these keywords (case-insensitive)
# Any job that doesn't match gets thrown out. Add/remove as needed.
TITLE_KEYWORDS = [
    "IAM",
    "PAM",
    "CyberArk",
    "Cyberark",
    "Identity",
    "Privileged Access",
    "Access Management",
    "Security Engineer",
    "Security Architect",
    "Cybersecurity",
    "Cyber Security",
    "Cloud Security",
    "Incident Response",
    "Penetration",
    "Pen Test",
    "SOC Analyst",
    "Threat Intelligence",
    "Information Security",
    "Security Consultant",
    "Security Analyst",
]

# =============================================================================
# QUICK EDITING GUIDE:
#
# 1. ADD A JOB ROLE:      Add to JOB_ROLES list
# 2. CHANGE JOB TYPE:     JOB_TYPE = "fulltime" | "contract" | None (all)
# 3. TOGGLE REMOTE:       REMOTE_ONLY = True | False
# 4. CHANGE EMAIL:        Update EMAIL_RECIPIENT
# 5. ADJUST DATE RANGE:   DAYS_BACK = 14 (2 weeks), 30 (1 month)
# 6. TOGGLE JOB BOARDS:   Set SCRAPE_DICE = False etc.
# =============================================================================
