# Homelab

Self-hosted services running via Docker Compose.

## Services

| Directory | Description |
|-----------|-------------|
| **ai/** | Ollama (local LLMs), SearXNG (web search), Open WebUI (AI chat interface) |
| **arr/** | *Arr stack: Prowlarr (indexers), Radarr (movies), Sonarr (TV), Jellyseerr (requests), Sabnzbd (usenet downloads) |
| **automation/** | n8n workflows, job scraper API (LinkedIn, RemoteOK), evolution-api (WhatsApp) |
| **books/** | Calibre & Calibre-web (ebooks), Kavita (comics/manga), Audiobookshelf (audiobooks & podcasts) |
| **homepage/** | Gethomepage — homelab dashboard and service launcher |
| **immich/** | Self-hosted photo and video backup |
| **music/** | Slskd (Soulseek), Navidrome (music server), Feishin (client), Soularr (automation) |
| **wireguard-qbit-vpn/** | qBittorrent behind Private Internet Access WireGuard VPN |

## Usage

From each directory, bring up services with:

```bash
docker compose up -d
```

Most stacks require a `.env` file — check for `example.env` in each directory.

## Automation

The **automation/** stack runs n8n for workflow automation and includes a job-search API that aggregates listings from LinkedIn, RemoteOK, Indeed, and more. Use n8n to build workflows that:

- Schedule job searches and filter results
- Send alerts to Slack, Discord, or email
- Store listings in a database or spreadsheet

See [automation/README.md](automation/README.md) for setup and job-search workflow details.
