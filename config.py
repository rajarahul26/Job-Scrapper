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

# Job boards to scrape (leave all True for maximum coverage)
SCRAPE_LINKEDIN = True
SCRAPE_INDEED = True
SCRAPE_GLASSDOOR = True
SCRAPE_ZIPRECRUITER = False  # Disabled - unreliable in current version
SCRAPE_GOOGLE = False        # Disabled - unreliable in current version

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
# 1. ADD A JOB ROLE:
#    Add to JOB_ROLES list, e.g., "Security Operations Manager"
#
# 2. CHANGE EMAIL RECIPIENT:
#    Update EMAIL_RECIPIENT = "newemail@gmail.com"
#
# 3. ADJUST HOW MANY DAYS BACK:
#    Change DAYS_BACK = 14 (for 2 weeks instead of 1)
#
# 4. EXCLUDE A JOB BOARD:
#    Set SCRAPE_LINKEDIN = False (etc.)
# =============================================================================
