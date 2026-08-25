import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watchly MovieBox Premium Rest Engine")

# CORS को Allow करना ताकि Netlify या React ब्लॉक न करे
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOVIEBOX_BASE = "https://inmoviebox.com"
HEADERS = {
    "User-Agent": "MovieBoxPro/16.2.1 (Android 12; Pixel 6)",
    "X-M-Version": "16.2.1",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://aoneroom.com"
}

@app.get("/api/v1/trending")
async def get_trending_feed():
    url = f"{MOVIEBOX_BASE}/home-api/list"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=HEADERS, timeout=10.0)
        return res.json()

@app.get("/api/v1/search")
async def search_moviebox(query: str):
    url = f"{MOVIEBOX_BASE}/search-api/search?keyword={query}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=HEADERS, timeout=10.0)
        return res.json()

@app.get("/api/v1/stream")
async def get_stream_links(id: str):
    url = f"{MOVIEBOX_BASE}/subject-api/get?subjectId={id}"
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=HEADERS, timeout=10.0)
        return res.json()
