from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from jobspy import scrape_jobs
import json, math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/jobs")
def search_jobs(
    query: str = Query(...),
    location: str = Query("United States"),
    limit: int = Query(10),
    hours: int = Query(720),
):
    try:
        df = scrape_jobs(
            site_name=["linkedin"],
            search_term=query,
            location=location,
            results_wanted=limit,
            hours_old=hours,
        )
        jobs = []
        for _, row in df.iterrows():
            salary = ""
            if row.get("min_amount") and not (isinstance(row["min_amount"], float) and math.isnan(row["min_amount"])):
                mn = int(row["min_amount"])
                mx = int(row.get("max_amount", mn))
                salary = f"${mn:,} - ${mx:,}"

            posted = str(row.get("date_posted", "")) if row.get("date_posted") else ""

            desc = str(row.get("description", "")) if row.get("description") and str(row.get("description")) != "nan" else ""
            desc = desc[:150] if desc else ""

            url = str(row.get("job_url", ""))
            if not url or url == "nan":
                continue

            jobs.append({
                "id": f"{row.get('site','?')}_{url.split('/')[-1].split('=')[-1]}",
                "title": str(row.get("title", "")),
                "company": str(row.get("company", "")),
                "location": str(row.get("location", "")),
                "salary": salary,
                "applyUrl": url,
                "source": str(row.get("site", "")).capitalize(),
                "postedDate": posted,
                "description": desc,
            })
        return {"jobs": jobs}
    except Exception as e:
        return {"jobs": [], "error": str(e)}
