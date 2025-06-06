import base64
import requests

# 1. Load image and convert to base64
with open("test_dataset/images/test_004.png", "rb") as img_file:
    base64_str = base64.b64encode(img_file.read()).decode("utf-8")

# 2. Send to FastAPI endpoint
url = "http://localhost:8000/extract"
response = requests.post(url, json={"image_base64": base64_str})

# 3. Print results
print("📦 Response JSON:")
print(response.json())
