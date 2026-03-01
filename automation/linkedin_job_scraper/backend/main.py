import re

from flask import Flask, request, jsonify
from jobspy import scrape_jobs
import math
from extractors.remoteok import extract_remoteok_jobs

app = Flask(__name__)


def clean_for_json(val):
    """Convert NaN/Inf and numpy types for JSON serialization."""
    if val is None:
        return None
    if hasattr(val, "item"):  # numpy scalar
        val = val.item()
    try:
        if isinstance(val, (int, float)) and (math.isnan(val) or math.isinf(val)):
            return None
    except (TypeError, ValueError):
        pass
    return val


def dataframe_to_records(df):
    """Convert pandas DataFrame to list of dicts with NaN handling."""
    records = []
    for _, row in df.iterrows():
        record = {}
        for col in df.columns:
            val = row[col]
            record[col] = clean_for_json(val)
        records.append(record)
    return records


@app.route("/jobs", methods=["GET", "POST"])
def get_jobs():
    if request.method == "GET":
        data = request.args
    else:
        data = request.get_json() or {}

    site_name = data.get("site_name", "linkedin")
    search_term = data.get("search_term", "software engineer")
    location = data.get("location", "")
    results_wanted = min(int(data.get("results_wanted", 100)), 100)
    job_type = data.get("job_type")  # fulltime, parttime, internship, contract
    is_remote = data.get("is_remote", "").lower() in ("true", "1", "yes")
    linkedin_fetch_description = data.get("fetch_description", "").lower() in ("true", "1", "yes")

    scrape_args = dict(
        # default site_name is all
        site_name=site_name,
        search_term=search_term,
        results_wanted=results_wanted,
        verbose=0,
        linkedin_fetch_description=linkedin_fetch_description,
    )
    if location:
        scrape_args["location"] = location
    if job_type:
        scrape_args["job_type"] = job_type
    if is_remote:
        scrape_args["is_remote"] = True

    try:
        jobs_df = scrape_jobs(**scrape_args)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    records = dataframe_to_records(jobs_df)
    return jsonify({"count": len(records), "jobs": records})

@app.route("/remoteok", methods=["GET", "POST"])
def get_remoteok_jobs():
    if request.method == "GET":
        data = request.args
    else:
        data = request.get_json() or {}

    # TODO: add keyword search instead of pulling all jobs

    keyword = data.get("keyword")  # None/empty = all jobs; e.g. "engineer" = filtered
    results_wanted = min(int(data.get("results_wanted", 10)), 100)
    jobs = extract_remoteok_jobs(keyword)[:results_wanted]

    # Add id derived from link URL (last path segment)
    for job in jobs:
        slug = job["link"].rstrip("/").split("/")[-1] if job.get("link") else ""
        match = re.search(r"-(\d+)$", slug)
        job["id"] = match.group(1) if match else slug or None
        job["position"] = (job.get("position") or "").lower()

    return jsonify({"count": len(jobs), "jobs": jobs})



@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
