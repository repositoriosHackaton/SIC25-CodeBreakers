FROM python:3.13.2-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install opencv-python-headless && \
    pip install -r requirements.txt && \
    rm -rf ~/.cache/pip && \
    apt-get update && apt-get install ffmpeg libsm6 libxext6  -y \
    build-essential && \
    rm -rf /var/lib/apt/lists/*


