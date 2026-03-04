"""
Simple FastAPI server that captures an image from rpicam when the endpoint is called.
Designed to run on a Raspberry Pi with rpicam-still (libcamera).
"""

import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="PlunkCam", description="Raspberry Pi camera capture API")

# rpicam-still binary (Raspberry Pi OS Bookworm+ uses rpicam-, older uses libcamera-)
RPICAM_STILL = "rpicam-still"


@app.get("/capture")
async def capture_image():
    """Capture a single JPEG from the Raspberry Pi camera and return it."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        output_path = tmp.name

    try:
        result = subprocess.run(
            [RPICAM_STILL, "-o", output_path, "-n"],  # -n = no preview
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode != 0:
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Camera capture failed",
                    "stderr": result.stderr or "Unknown error",
                },
            )

        path = Path(output_path)
        if not path.exists() or path.stat().st_size == 0:
            return JSONResponse(
                status_code=503,
                content={"error": "No image captured"},
            )

        image_bytes = path.read_bytes()
        return Response(content=image_bytes, media_type="image/jpeg")
    except FileNotFoundError:
        return JSONResponse(
            status_code=503,
            content={
                "error": "rpicam-still not found. Install with: sudo apt install rpicam-apps",
            },
        )
    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=504,
            content={"error": "Camera capture timed out"},
        )
    finally:
        Path(output_path).unlink(missing_ok=True)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
