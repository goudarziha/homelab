import requests


def extract_remoteok_jobs(keyword=None):
    """Scrape job listings from RemoteOK. Uses the public JSON API at remoteok.com/api."""
    url = "https://remoteok.com/api"
    if keyword:
        # API accepts single-word tags (e.g. "engineer", "software")
        tag = keyword.strip().split()[-1] if keyword.strip() else None
        if tag:
            url = f"https://remoteok.com/api?tag={tag}"

    resp = requests.get(url, headers={"User-Agent": "RemoteOK-JobScraper/1.0"})
    results = []

    if resp.status_code != 200:
        return results

    try:
        data = resp.json()
    except ValueError:
        return results

    # First element is API metadata; rest are job listings
    for item in data[1:]:
        if not isinstance(item, dict) or "id" not in item:
            continue

        slug = item.get("slug", "")
        job_id = item.get("id", "")
        link = item.get("url") or (
            f"https://remoteok.com/live/{slug}" if slug else f"https://remoteok.com/live/{job_id}"
        )
        company = item.get("company") or ""
        position = item.get("position") or ""
        location = item.get("location") or item.get("region") or "Worldwide"

        if company and position:
            results.append({
                "link": link,
                "company": str(company).strip(),
                "position": str(position).strip(),
                "location": str(location).strip() if location else "Worldwide",
                "date": item.get("date"),
                "tags": item.get("tags", []),
            })

    return results