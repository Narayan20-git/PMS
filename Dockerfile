# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Set working directory ----------
WORKDIR /app

# ---------- Copy dependency files ----------
COPY requirements.txt .

# ---------- Install dependencies ----------
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy application code ----------
COPY . .

# ---------- Expose FastAPI default port ----------
EXPOSE 8080

# ---------- Set environment variables ----------
# You can override these in Cloud Run
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# ---------- Run FastAPI with Uvicorn ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
