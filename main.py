import httpx
import time
import hashlib
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watchly Global Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. ग्लोबल सर्वर (जो रेंडर को ब्लॉक नहीं करता)
MOVIEBOX_BASE = "https://aoneroom.com"

def get_headers():
    timestamp = str(int(time.time()))
    key = hashlib.md5(timestamp[::-1].encode()).hexdigest()
    return {
        "User-Agent": "MovieBoxPro/16.2.1 (Android 12; Pixel 6)",
        "Accept": "application/json",
        "X-Client-Token": f"{timestamp},{key}",
        "Referer": "https://www.movieboxpro.app/"
    }

@app.get("/api/v1/moviebox/search")
async def search_proxy(query: str):
    # ग्लोबल सर्वर पर रिक्वेस्ट भेजना
    url = f"{MOVIEBOX_BASE}/search-api/search?keyword={query}"
    async with httpx.AsyncClient(verify=False) as client:
        try:
            resp = await client.get(url, headers=get_headers(), timeout=15.0)
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": f"Global Server Error: {str(e)}"}

@app.get("/api/v1/moviebox/stream")
async def stream_proxy(id: str):
    url = f"{MOVIEBOX_BASE}/subject-api/get?subjectId={id}"
    async with httpx.AsyncClient(verify=False) as client:
        try:
            resp = await client.get(url, headers=get_headers(), timeout=15.0)
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": "Stream Link Failed"}
