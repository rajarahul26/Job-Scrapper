#!/usr/bin/env python3
# =============================================================================
# SCRAPER.PY - MAIN JOB SCRAPER USING JOBSPY
# =============================================================================

import os
import sys
import csv
import json
from datetime import datetime, timedelta
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# JobSpy library
from jobspy import scrape_jobs

# Import config
from config import (
    JOB_ROLES,
    LOCATIONS,
    DAYS_BACK,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    EMAIL_RECIPIENT,
    OUTPUT_DIR,
    OUTPUT_FILENAME_PREFIX,
    RESULTS_PER_ROLE,
    EMAIL_SUBJECT,
    SCRAPE_LINKEDIN,
    SCRAPE_INDEED,
    SCRAPE_GLASSDOOR,
    SCRAPE_ZIPRECRUITER,
    SCRAPE_GOOGLE,
)


def get_job_boards():
    """Return list of job boards to scrape based on config"""
    boards = []
    if SCRAPE_LINKEDIN:
        boards.append("linkedin")
    if SCRAPE_INDEED:
        boards.append("indeed")
    if SCRAPE_GLASSDOOR:
        boards.append("glassdoor")
    if SCRAPE_ZIPRECRUITER:
        boards.append("ziprecruiter")
    if SCRAPE_GOOGLE:
        boards.append("google")
    return boards


def scrape_all_jobs() -> List[Dict]:
    """Scrape jobs for all configured roles and locations"""
    all_jobs = []

    print(f"🔍 Starting job scrape for {len(JOB_ROLES)} roles...")
    print(f"📍 Locations: {', '.join(LOCATIONS)}")
    print(f"📅 Looking back: {DAYS_BACK} days")
    print(f"🔗 Job boards: {', '.join(get_job_boards())}\n")

    for role in JOB_ROLES:
        for location in LOCATIONS:
            try:
                print(f"   Scraping: {role} in {location}...")

                jobs = scrape_jobs(
                    site_name=get_job_boards(),
                    search_term=role,
                    location=location,
                    results_wanted=RESULTS_PER_ROLE,
                    hours_old=DAYS_BACK * 24,  # Convert days to hours
                    country_indeed="USA",
                )

                # Convert to list if it's a DataFrame
                if hasattr(jobs, 'to_dict'):
                    jobs = jobs.to_dict('records')

                all_jobs.extend(jobs)
                print(f"      ✓ Found {len(jobs)} jobs")

            except Exception as e:
                print(f"      ✗ Error scraping {role}: {str(e)}")
                continue

    print(f"\n✅ Total jobs found: {len(all_jobs)}\n")
    return all_jobs


def save_to_csv(jobs: List[Dict]) -> str:
    """Save jobs to CSV file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Create filename with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{OUTPUT_DIR}/{OUTPUT_FILENAME_PREFIX}-{today}.csv"

    if not jobs:
        print("⚠️  No jobs to save!")
        return filename

    # Get all unique keys from jobs
    fieldnames = set()
    for job in jobs:
        fieldnames.update(job.keys())
    fieldnames = sorted(list(fieldnames))

    # Write CSV
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)

        print(f"💾 Saved {len(jobs)} jobs to: {filename}")
        return filename

    except Exception as e:
        print(f"❌ Error saving CSV: {str(e)}")
        return None


def send_email(jobs: List[Dict], csv_filename: str):
    """Send results email to recipient"""
    if not jobs:
        print("⚠️  No jobs to email!")
        return

    try:
        # Create email body
        email_body = create_email_body(jobs)

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT

        # Attach HTML content
        msg.attach(MIMEText(email_body, 'html'))

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email sent successfully to {EMAIL_RECIPIENT}")

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("   Make sure your Gmail App Password is correct (see README.md)")


def create_email_body(jobs: List[Dict]) -> str:
    """Create HTML email body with job summary"""

    # Count jobs by title
    job_titles = {}
    for job in jobs:
        title = job.get('title', 'Unknown')
        job_titles[title] = job_titles.get(title, 0) + 1

    # Create job summary rows
    summary_rows = ''.join([
        f"<tr><td style='padding: 10px; border-bottom: 1px solid #ddd;'><strong>{title}</strong></td><td style='padding: 10px; border-bottom: 1px solid #ddd; text-align: center;'>{count}</td></tr>"
        for title, count in sorted(job_titles.items(), key=lambda x: x[1], reverse=True)
    ])

    # Count by source
    sources = {}
    for job in jobs:
        source = job.get('site', 'Unknown')
        sources[source] = sources.get(source, 0) + 1

    source_rows = ''.join([
        f"<tr><td style='padding: 10px; border-bottom: 1px solid #ddd;'>{source}</td><td style='padding: 10px; border-bottom: 1px solid #ddd; text-align: center;'>{count}</td></tr>"
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)
    ])

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            .summary {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .timestamp {{ color: #7f8c8d; font-size: 12px; margin-top: 20px; }}
            .note {{ background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Weekly Cybersecurity Job Scraper Results</h1>

            <div class="summary">
                <p><strong>📊 Total Jobs Found:</strong> {len(jobs)}</p>
                <p><strong>📅 Period:</strong> Last {DAYS_BACK} day(s)</p>
                <p><strong>🕐 Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <h2>📌 Jobs by Role</h2>
            <table>
                <tr>
                    <th>Job Title</th>
                    <th style="text-align: center;">Count</th>
                </tr>
                {summary_rows}
            </table>

            <h2>🔗 Jobs by Source</h2>
            <table>
                <tr>
                    <th>Job Board</th>
                    <th style="text-align: center;">Count</th>
                </tr>
                {source_rows}
            </table>

            <div class="note">
                <strong>📥 Full Results:</strong> See attached CSV file for complete job details including links, salaries, and descriptions.
            </div>

            <h2>🔍 Roles Searched</h2>
            <ul>
                {''.join([f'<li>{role}</li>' for role in JOB_ROLES])}
            </ul>

            <p class="timestamp">
                <em>This email was generated by your automated job scraper.
                <br>Next run: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}</em>
            </p>
        </div>
    </body>
    </html>
    """

    return html


def main():
    """Main execution"""
    print("=" * 60)
    print("🚀 CYBERSECURITY JOB SCRAPER")
    print("=" * 60 + "\n")

    # Scrape jobs
    jobs = scrape_all_jobs()

    if not jobs:
        print("❌ No jobs found. Exiting.")
        return

    # Save to CSV
    csv_filename = save_to_csv(jobs)

    # Send email
    if EMAIL_SENDER and EMAIL_PASSWORD and EMAIL_RECIPIENT:
        send_email(jobs, csv_filename)
    else:
        print("⚠️  Email credentials not configured. Skipping email.")

    print("\n" + "=" * 60)
    print("✅ JOB SCRAPE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
