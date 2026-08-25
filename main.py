import httpx
import time
import hashlib
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Watchly MovieBox Pro Pure Engine")

# CORS Setup - ताकि आपकी Netlify React ऐप ब्लॉक न हो
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# मूवीबॉक्स प्रो का ऑफिशियल एशिया/इंडिया सर्वर गेटवे
MOVIEBOX_BASE = "https://inmoviebox.com"

def generate_moviebox_signature():
    """मूवीबॉक्स के नए सिक्योरिटी ब्लॉक को बाईपास करने के लिए क्रिप्टोग्राफिक टाइमस्टैम्प टोकन बनाना"""
    timestamp = str(int(time.time()))
    # मूवीबॉक्स के ऐप का इंटरनल md5 reversed_timestamp मैकेनिज्म
    reversed_ts = timestamp[::-1]
    client_token = hashlib.md5(reversed_ts.encode()).hexdigest()
    return f"{timestamp},{client_token}"

# बिल्कुल असली और करंट मोबाइल ऐप हेडर्स
HEADERS = {
    "User-Agent": "MovieBoxPro/16.2.1 (Android 12; Pixel 6)",
    "X-M-Version": "16.2.1",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Referer": "https://aoneroom.com",
    "Connection": "keep-alive"
}

@app.get("/api/v1/moviebox/search")
async def search_moviebox(query: str):
    """आपके फ्रंटएंड से जो TMDB/IMDb का मूवी नेम आएगा, उसे यहाँ भेजकर मूवीबॉक्स की असली ID निकालें"""
    url = f"{MOVIEBOX_BASE}/search-api/search?keyword={query}"
    
    current_headers = HEADERS.copy()
    current_headers["X-Client-Token"] = generate_moviebox_signature()
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=current_headers, timeout=12.0)
            return res.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail="MovieBox Search Server Busy")

@app.get("/api/v1/moviebox/stream")
async def get_moviebox_stream(id: str):
    """मूवीबॉक्स की ID पास करके सीधे सिंक होने वाले रॉ वीडियो लिंक्स (.mp4 / .m3u8) और सबटाइटल्स पाना"""
    url = f"{MOVIEBOX_BASE}/subject-api/get?subjectId={id}"
    
    current_headers = HEADERS.copy()
    current_headers["X-Client-Token"] = generate_moviebox_signature()
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=current_headers, timeout=12.0)
            return res.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail="MovieBox Streaming Cluster Locked")
