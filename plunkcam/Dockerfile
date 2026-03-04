FROM python:3.12-slim

# rpicam-apps is Raspberry Pi OS specific. For Docker on Pi:
# - Use Raspberry Pi OS base, or
# - Build on-device: docker build -t plunkcam . --build-arg TARGETARCH=arm64
# - Or run natively: python main.py (with rpicam-apps installed via apt)
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
