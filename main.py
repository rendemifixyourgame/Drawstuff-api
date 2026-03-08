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

@app.get("/convert")
def convert(url: str = Query(...), width: int = 64, height: int = 64):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch image from URL")

    try:
        img = Image.open(BytesIO(response.content)).convert("L")
        img = img.resize((width, height), Image.LANCZOS)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to process image")

    pixels = []
    for y in range(height):
        for x in range(width):
            brightness = img.getpixel((x, y))
            color = "white" if brightness >= 128 else "black"
            pixels.append({"x": x, "y": y, "color": color})

    return {"width": width, "height": height, "pixels": pixels}
