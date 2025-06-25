````md
# 🪪 IDCard Content Extractor – AI-Powered OCR + NLP Microservice

An intelligent, full-stack microservice to extract structured fields from **student ID cards** using a hybrid architecture: OCR (Tesseract), Regex, spaCy NER (custom trained), and Fallback heuristics.

> 🚀 Developed as part of a **Summer Internship @ Turtil**, this project is offline-capable, Dockerized, and includes a clean UI + robust JSON API for high-accuracy predictions even from noisy ID card formats.

---

## 📸 Sample JSON Output

```json
{
  "user_id": "stu_4821",
  "extracted_fields": {
    "name": "Anjali Sharma",
    "college": "RGMCET Nandyal",
    "roll_number": "21RGME1032",
    "branch": "Mechanical Engineering",
    "valid_upto": "2025"
  },
  "confidence_score": 0.91,
  "missing_fields": ["branch"],
  "status": "partial_success"
}
````

---

## ✅ Features

* 🎯 Extracts the following fields:

  * `name`, `college`, `branch`, `roll_number`, `valid_upto`
* 🧠 Combines:

  * Tesseract OCR
  * Regex Extraction
  * spaCy NER (trained on aligned ID OCR text)
  * Fallback keyword-based extraction
* 📊 Includes:

  * `confidence_score`, `missing_fields`, `status`: success/partial\_success/failure
* 🖥️ Simple Web UI for upload and preview
* 🔁 Fully Dockerized
* 🌐 Deployed to Render (Cloud)


## 🧩 Tech Stack

| Layer          | Tools Used                     |
| -------------- | ------------------------------ |
| **Backend**    | FastAPI, Python                |
| **OCR**        | Tesseract, OpenCV              |
| **NLP/NER**    | spaCy (custom model), Regex    |
| **Frontend**   | HTML, Tailwind CSS, Vanilla JS |
| **Deployment** | Docker, Render                 |
| **Others**     | Uvicorn, Base64, JSON, Jinja2  |

## 🗂️ Project Structure

```bash
card_extractor/
├── app/
│   ├── main.py                # FastAPI routes
│   ├── templates/upload.html  # Frontend UI
├── model/
│   ├── ocr.py                 # OCR wrapper
│   ├── regex_extractor.py    # Rule-based fields
│   ├── ner_extractor.py      # spaCy NER
│   ├── fallback_extractor.py # Keyword fallback
├── utils/
│   ├── generate_training_data.py  # For NER training
├── dataset/
│   ├── images/               # Training/test images
│   ├── labels/               # Ground truth JSONs
├── ner_model/                # Trained model
├── train_spacy.py            # Train NER model
├── evaluate_accuracy.py      # Evaluate predictions
├── test_pipeline.py          # CLI tester
├── test_api.py               # Test endpoint
├── requirements.txt
├── Dockerfile
```


## 🔧 Setup Instructions

### 1. Clone or Download

```bash
git clone https://github.com/<your-username>/idcard-extractor.git
cd idcard-extractor
```


### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```


### 3. Install Requirements

```bash
pip install -r requirements.txt
```

> ✅ Make sure you have **Tesseract OCR** installed and accessible via PATH.


### 4. Run Locally

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/upload](http://localhost:8000/upload)
OR test APIs via [http://localhost:8000/docs](http://localhost:8000/docs)


### 5. Evaluate Accuracy

```bash
python evaluate_accuracy.py
```

Compares predictions with ground truth in `/dataset/labels` and prints field-wise accuracy.


### 6. Docker Deployment

```bash
docker build -t idcard-extractor .
docker run -p 8000:8000 idcard-extractor
```


### 7. Test in Postman

* Method: POST
* URL: `http://localhost:8000/extract`
* Body: Raw JSON

```json
{
  "image_base64": "<your_base64_image_here>"
}
```


## 📚 Internship Timeline Summary

| Week       | Tasks Completed                                                          |
| ---------- | ------------------------------------------------------------------------ |
| **Week 1** | Setup FastAPI, OCR with Tesseract, base folder structure                 |
| **Week 2** | Added Regex, Fallbacks, UI, routing logic                                |
| **Week 3** | Trained custom spaCy NER model, generated aligned training data          |
| **Week 4** | Dockerization, Render deployment, confidence scoring, final testing      |
| **Final**  | Achieved 85% accuracy with field augmentation, wrote documentation + PPT |


## 🎯 Accuracy Improvements

| Stage                   | Accuracy    |
| ----------------------- | ----------- |
| Initial (Regex Only)    | \~70%       |
| With spaCy NER          | \~80%       |
| With Field Augmentation | ✅ **\~85%** |

* Variants handled:

  * `"Roll No"`, `"Htno"`, `"Card No"`
  * `"CSE"`, `"CSE (AI&ML)"`, `"CSED"`, etc.


## 🧪 Testing Utilities

* `test_pipeline.py` → CLI image extractor
* `evaluate_accuracy.py` → Accuracy reporting
* `test_api.py` → FastAPI endpoint tester
* `/docs` → Swagger UI auto-generated


## 🧠 Challenges Solved

* NER misalignment → Resolved via offset-aware `generate_training_data.py`
* Incorrect matches → Introduced fallback & stricter regex
* Deployment bugs → Fixed with Uvicorn + Docker optimization

---

## V2 Version Updates


### 🔄 **Version: v2 – Field Normalization & Accuracy Upgrade**

#### 📌 Description:

Version **v2** introduces major improvements to the ID Card Content Extraction pipeline by adding **normalization logic** for extracted fields and refining the overall flow for better accuracy, consistency, and reliability.

---

### ✅ **What’s New in v2**

| Feature                                    | Description                                                                                                                                                       |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🧠 **Field Normalization**                 | Added `normalize_name`, `normalize_college`, `normalize_branch`, and `normalize_roll_number` to correct inconsistencies, typos, and duplicates in extracted text. |
| ⚙️ **Integrated Normalization in FastAPI** | All normalization functions are now applied in `main.py` (backend API) before sending the final output to frontend/API consumers.                                 |
| 📊 **Improved Accuracy**                   | Accuracy improved from **80% → 91%** through better post-processing, fallback logic, and normalization of field variants.                                         |
| 🧪 **Test Coverage**                       | Updated `test_pipeline.py`, `evaluate_accuracy.py`, and ensured consistent outputs across CLI, frontend, and API.                                                 |
| 🔍 **Edge Case Handling**                  | Resolved issues where fields like name/college were not detected due to inconsistent OCR/NER results.                                                             |
| 📁 **Cleaner Output**                      | Ensured that missing or unknown fields are gracefully handled and returned as `"Unknown"` instead of causing errors.                                              |

---

### 🛠️ Fixes

* 🐞 Fixed `NoneType` `.strip()` errors when missing fields were being normalized.
* 🐞 Fixed inconsistent field matching due to OCR casing or spacing issues.
* 🐞 Improved branch and roll number disambiguation with rule-based normalization.

---

### 📈 Summary:

This version strengthens the pipeline with smart normalization, leading to **cleaner data, better matching, and higher field-level accuracy.**


## 🔮 Future Enhancements

* Switch NER to HuggingFace Transformers (BERT)
* Integrate EasyOCR for complex cards
* Add multilingual support (Telugu, Hindi)
* User authentication + history dashboard

 © 2025 \[Vinay Teja @ Turtil]

