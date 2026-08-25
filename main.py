import httpx
import time
import hashlib
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watchly Global Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Use the specific API6 cluster which is more permissive for cloud IPs
MOVIEBOX_BASE = "https://aoneroom.com"

def get_headers():
    timestamp = str(int(time.time()))
    key = hashlib.md5(timestamp[::-1].encode()).hexdigest()
    return {
        "User-Agent": "MovieBoxPro/16.2.1 (Android 12; Pixel 6)",
        "Accept": "application/json",
        "X-Client-Token": f"{timestamp},{key}",
        "Referer": "https://api6.aoneroom.com/"
    }

async def fetch_with_retry(url):
    # Retry logic to handle DNS flickers on Render
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        for attempt in range(3):
            try:
                resp = await client.get(url, headers=get_headers(), timeout=15.0)
                resp.raise_for_status()
                return resp.json()
            except httpx.ConnectError:
                # If connection fails, wait 1s and retry
                await asyncio.sleep(1)
            except Exception as e:
                if attempt == 2:
                    raise HTTPException(status_code=502, detail=f"Upstream Error: {str(e)}")
    return {"status": "error", "message": "Failed to connect to MovieBox"}

@app.get("/api/v1/moviebox/search")
async def search_proxy(query: str):
    url = f"{MOVIEBOX_BASE}/search-api/search?keyword={query}"
    return await fetch_with_retry(url)

@app.get("/api/v1/moviebox/stream")
async def stream_proxy(id: str):
    url = f"{MOVIEBOX_BASE}/subject-api/get?subjectId={id}"
    return await fetch_with_retry(url)
