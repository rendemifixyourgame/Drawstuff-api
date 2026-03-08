from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@app.get("/convert")
def convert(url: str = Query(...), width: int = 64, height: int = 64):
    try:
        response = requests.get(url, timeout=10, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: {str(e)}")

    try:
        img = Image.open(BytesIO(response.content)).convert("L")
        img = img.resize((width, height), Image.LANCZOS)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")

    pixels = []
    for y in range(height):
        for x in range(width):
            brightness = img.getpixel((x, y))
            color = "white" if brightness >= 128 else "black"
            pixels.append({"x": x, "y": y, "color": color})

    return {"width": width, "height": height, "pixels": pixels}
