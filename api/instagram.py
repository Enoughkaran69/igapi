from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader

app = FastAPI()

# Enable CORS for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_video_metadata(reel_url: str):
    """Extract metadata from Instagram reel"""
    try:
        L = instaloader.Instaloader()
        shortcode = reel_url.strip("/").split("/")[-1]  # Extract shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_video:
            metadata = {
                "shortcode": post.shortcode,
                "video_url": post.video_url,
                "caption": post.caption,
                "likes": post.likes,
                "comments": post.comments,
                "date_utc": str(post.date_utc),
                "thumbnail_url": post.url,
                "video_view_count": post.video_view_count,
            }
            return metadata
        else:
            return None
    except Exception as e:
        raise ValueError(f"Failed to fetch video: {str(e)}")

@app.get("/download")
async def download_reel(url: str = Query(..., description="Instagram reel URL")):
    """API endpoint to get Instagram reel metadata"""
    try:
        metadata = extract_video_metadata(url)
        if metadata:
            return metadata
        else:
            return {"error": "This is not a video post."}
    except Exception as e:
        return {"error": str(e)}

# Required for Vercel to recognize the app
api = app
