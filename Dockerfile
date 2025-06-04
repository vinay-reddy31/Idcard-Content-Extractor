# 🔹 Step 1: Base Python image
FROM python:3.10-slim

# 🔹 Step 2: Install system packages (Tesseract + libGL for OpenCV) && shrink the image size
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 🔹 Step 3: Set working directory
WORKDIR /app

# 🔹 Step 4: Copy your app files into the image
COPY . /app

# 🔹 Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Step 6: Download spaCy model
RUN python -m spacy download en_core_web_sm

# 🔹 Step 7: Expose FastAPI port
EXPOSE 8000

# 🔹 Step 8: Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

