FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY models/best.pt models/best.pt

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app/streamlit.py", "--server.address=0.0.0.0", "--server.port=8501"]