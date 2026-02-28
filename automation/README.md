# Automation

Workflow automation and job-search tooling for the homelab.

## Services

| Service               | Port | Description                               |
|-----------------------|------|-------------------------------------------|
| **n8n**               | 5678 | Workflow automation (visual node editor)  |
| **linkedin_job_scraper** | 5001 | Job listings API (LinkedIn, RemoteOK, etc.) |
| **postgres**           | —    | Database for n8n                          |
| **evolution-api**     | 8080 | WhatsApp API                              |

## Setup

1. Copy `example.env` to `.env` and configure:
   ```bash
   cp example.env .env
   ```

2. Start services:
   ```bash
   docker compose up -d
   ```

3. Access n8n at http://localhost:5678 (or your configured domain).

## Job-Search Workflow (n8n)

The job scraper API is designed to be used from n8n workflows. Typical workflow:

1. **Trigger** — Schedule (Cron) or manual
2. **HTTP Request** — Call the job scraper endpoints
3. **Process** — Filter, transform, or store results

### API Endpoints

**JobSpy (LinkedIn, Indeed, Glassdoor, etc.)** — `GET/POST http://linkedin_job_scraper:5000/jobs`

| Param            | Description                    |
|------------------|--------------------------------|
| `search_term`    | e.g. "software engineer"       |
| `location`       | e.g. "San Francisco"           |
| `results_wanted` | 1–100 (default 20)              |
| `site_name`      | linkedin, indeed, glassdoor…   |

**RemoteOK** — `GET/POST http://linkedin_job_scraper:5000/remoteok`

| Param     | Description                                  |
|-----------|----------------------------------------------|
| `keyword` | Optional tag filter (e.g. "engineer", "design") |

### Example n8n Workflow

1. **Schedule Trigger** — Run daily at 9:00
2. **HTTP Request** — `GET http://linkedin_job_scraper:5000/remoteok?keyword=software`
3. **HTTP Request** — `GET http://linkedin_job_scraper:5000/jobs?search_term=software%20engineer&results_wanted=20`
4. **Merge** — Combine results from both sources
5. **Filter** — Exclude jobs you’ve already seen (e.g. via Airtable, Notion, or a local DB)
6. **Actions** — Save to database, send to Slack/Discord, or email digest

From inside the Docker network, use the service name `linkedin_job_scraper` as the host. From your machine, use `localhost:5001`.
