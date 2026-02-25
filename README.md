# Homelab

Self-hosted services running via Docker Compose.

## Services

| Directory | Description |
|-----------|-------------|
| **ai/** | Ollama (local LLMs), SearXNG (web search), Open WebUI (AI chat interface) |
| **arr/** | *Arr stack: Prowlarr (indexers), Radarr (movies), Sonarr (TV), Jellyseerr (requests), Sabnzbd (usenet downloads) |
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
