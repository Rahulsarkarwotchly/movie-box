import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watchly Box REST Engine")

# CORS को पूरी तरह से Allow करना
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# अपडेटेड मूवीबॉक्स ग्लोबल सर्वर्स
MOVIEBOX_BASE = "https://inmoviebox.com"

# बिल्कुल असली और करंट मोबाइल ऐप हेडर्स
HEADERS = {
    "User-Agent": "MovieBoxPro/16.2.1 (Android 12; Pixel 6; Build/SD1A.210817.036)",
    "X-M-Version": "16.2.1",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://aoneroom.com",
    "Accept-Language": "hi-IN,en-US;q=0.9",
    "Connection": "keep-alive"
}

@app.get("/api/v1/trending")
async def get_trending_feed():
    url = f"{MOVIEBOX_BASE}/home-api/list"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=HEADERS, timeout=12.0)
            return res.json()
        except Exception as e:
            return {"status": "error", "message": "MovieBox cluster timed out. Try again."}

@app.get("/api/v1/search")
async def search_moviebox(query: str):
    url = f"{MOVIEBOX_BASE}/search-api/search?keyword={query}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=HEADERS, timeout=12.0)
            return res.json()
        except Exception as e:
            return {"status": "error", "message": "Search cluster busy."}

@app.get("/api/v1/stream")
async def get_stream_links(id: str):
    url = f"{MOVIEBOX_BASE}/subject-api/get?subjectId={id}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=HEADERS, timeout=12.0)
            return res.json()
        except Exception as e:
            return {"status": "error", "message": "Streaming links locked."}
