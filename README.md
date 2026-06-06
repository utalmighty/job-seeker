# Job Seeker - Automated Job Search Alerts

A Python script that automatically searches for job postings on company Workday portals with a specific keyword and sends Discord notifications for new postings found today.

## Overview

This script:
- Reads a CSV file containing company information (company names, Workday URLs, and location preferences)
- Searches each company's Workday portal for jobs matching your search keyword
- Filters results to show only jobs posted today
- Sends Discord notifications with matching job listings
- Can be scheduled to run automatically via cron

## Prerequisites

- Python 3.x
- `requests` library (`pip install requests`)
- A Discord server with a webhook configured
- Company Workday URLs and location identifiers

## Setup Instructions

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Configure Environment Variables (Optional)

The script has default values but can be customized with environment variables:

| Variable | Description | Default Value |
|----------|-------------|----------------|
| `SEARCH_TEXT` | Job search keyword | `Spring boot` |
| `CSV_PATH` | Path to CSV file with company data | `./sample.csv` |
| `DISCORD_WEBHOOK` | Discord webhook URL for notifications | Built-in webhook (set your own for production) |

### 3. Create Your CSV File

Create a CSV file with the following format:

```
CompanyName,Workday-URL,Location-Facet-Key,Location-ID-1,Location-ID-2,Location-ID-3
```

**Important:** The Location-Facet-Key must match the key used in the company's Workday API (e.g., `locations`, `locationCountry`, `primaryLocation`).

#### How to Find Workday URL and Location Facets

1. Go to the company's careers page (usually in their Workday portal)
2. Open your browser's Developer Tools (`F12` or `Cmd+Option+I`)
3. Go to the **Network** tab
4. Search for a job to trigger a network request
5. Look for a request to a Workday endpoint (usually a POST request)
6. Copy the request URL - this is your Workday URL
7. In the request payload, find the `appliedFacets` section
8. Note the **key name** (e.g., `locations` or `locationCountry`) - this is your Location-Facet-Key
9. Note the **values** for that key - these are your Location-IDs

### 4. Set Up Discord Webhook (Optional)

1. Open your Discord server settings
2. Go to **Webhooks**
3. Click **Create Webhook** and name it (e.g., "Job Alerts")
4. Copy the webhook URL
5. Set `DISCORD_WEBHOOK` environment variable to this URL

### 5. Run the Script

#### Manual Run (Using Defaults)

```bash
python script.py
```

#### Manual Run (Custom Settings)

```bash
export SEARCH_TEXT="Java"
export CSV_PATH="/path/to/your/sample.csv"
export DISCORD_WEBHOOK="https://discordapp.com/api/webhooks/..."

python script.py
```

#### Scheduled Run (Cron)

To run the script automatically, add it to your crontab:

```bash
crontab -e
```

Add a line to run the script at a specific time (example: daily at 11 PM):

```
0 23 * * * export SEARCH_TEXT="Java" && export CSV_PATH="/home/utalmighty/job-seeker/sample.csv" && export DISCORD_WEBHOOK="your_webhook_url" && /usr/bin/python3 /home/utalmighty/job-seeker/script.py
```

**Note:** Use full paths and set environment variables within the cron command.

## CSV Format Details

- **Column 1:** Company name (e.g., "Google")
- **Column 2:** Company's Workday job search URL
- **Column 3:** Location Facet Key (the API parameter name, e.g., `locations`, `locationCountry`, `primaryLocation`)
- **Columns 4+:** Location IDs (the actual location values to search in)

## How It Works

1. Reads all companies from your CSV file
2. For each company, makes a POST request to their Workday API with:
   - The specified location facet key and location IDs
   - Search text
   - Limit of 20 results
3. Filters jobs to only include those posted today
4. Sends Discord messages for each matching job found

## Troubleshooting

**No results found?**
- Verify your Workday URL is correct
- Check that location facets match the company's Workday API
- Ensure `SEARCH_TEXT` matches job titles in the portal

**Discord notifications not sending?**
- Verify the webhook URL is correct
- Check Discord server webhook permissions
- If `DISCORD_WEBHOOK` is not set, the script runs without sending notifications

**Script not running from cron?**
- Use absolute paths (not relative paths or `~`)
- Ensure Python is accessible at the specified path
- Check cron logs: `log stream --predicate 'process == "cron"'` (macOS)
- Test by running the command directly in terminal first

## Example Output

When a matching job is found, you'll receive a Discord notification:

```
**Google** posted job with keyword *Java* Job ID: `...`
```