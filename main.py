from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from moviebox_api import Moviebox

app = FastAPI(title="Watchly Engine")

# CORS (ताकि Netlify ब्लॉक न करे)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# लाइब्रेरी को इनिशियलाइज़ करें
mb = Moviebox()

@app.get("/api/v1/moviebox/search")
def search_content(query: str):
    try:
        # यह लाइब्रेरी ऑटोमैटिकली बेस्ट सर्वर से सर्च करेगी
        results = mb.search(query)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/moviebox/trending")
def get_trending():
    try:
        # होमपेज / ट्रेंडिंग कंटेंट
        trending = mb.home() 
        return {"status": "success", "data": trending}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/moviebox/stream")
def get_stream(id: str):
    try:
        # यह सीधे रॉ लिंक्स (720p/1080p) निकालेगा
        # नोट: लाइब्रेरी में ID पास करते समय ध्यान रखें
        links = mb.get_movie(id) 
        return {"status": "success", "data": links}
    except Exception as e:
        return {"status": "error", "message": "Link Extraction Failed"}
