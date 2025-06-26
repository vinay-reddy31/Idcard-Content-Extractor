# app/main.py
from fastapi import UploadFile, File, Request, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# 🔽 Import normalizers
from model.branch_normalizer import normalize_branch
from model.roll_number_normalizer import normalize_roll_number
from model.college_normalizer import normalize_college
from model.name_normalizer import normalize_name

from app.schemas import ExtractRequest, ExtractResponse
from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract

import base64
import tempfile

app = FastAPI(title="ID Card Extractor", version="1.0")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def handle_upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode("utf-8")

        extract_request = ExtractRequest(image_base64=image_base64)
        response = extract_info(extract_request)

        return JSONResponse(content={"result": response.extracted_fields})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract", response_model=ExtractResponse)
def extract_info(request: ExtractRequest):
    try:
        print("From realdata")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_img.write(base64.b64decode(request.image_base64))
            temp_img_path = temp_img.name

        text = image_to_text(temp_img_path)
        cleaned_text = text.replace("\n", " ").replace("  ", " ")

        regex_output = extract_fields(text)["extracted_fields"]
        ner_output = extract_entities(cleaned_text)
        fallback_output = fallback_extract(cleaned_text)

        final_output = regex_output.copy()
        final_output.update({k: v for k, v in ner_output.items() if v})

        for k, v in fallback_output.items():
            if not final_output.get(k):
                final_output[k] = v

        print("Merged fields:", final_output)

        required_fields = ["name", "college", "branch", "roll_number", "valid_upto"]
        missing = []
        for field in required_fields:
            raw_value = final_output.get(field)

            if not raw_value or str(raw_value).strip() == "":
                final_output[field] = "Unknown"
                missing.append(field)
                continue

            value = str(raw_value).strip()

            if field == "branch":
                final_output[field] = normalize_branch(value)
            elif field == "roll_number":
                final_output[field] = normalize_roll_number(value)
            elif field == "college":
                final_output[field] = normalize_college(value)
            elif field == "name":
                final_output[field] = normalize_name(value)
            else:
                final_output[field] = value

        # Status logic
        if len(missing) == len(required_fields):
            status = "failure"
        elif missing:
            status = "partial_success"
        else:
            status = "success"

        confidence_score = round(1 - len(missing) / len(required_fields), 2)
        user_id = "stu_" + str(abs(hash(text)) % 10000)

        return {
            "user_id": user_id,
            "extracted_fields": final_output,
            "confidence_score": confidence_score,
            "missing_fields": missing,
            "status": status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def version_info():
    return {
        "model_version": "1.0.0",
        "config_version": "1.0.0"
    }

