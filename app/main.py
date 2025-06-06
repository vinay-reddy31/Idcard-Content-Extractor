# app/main.py
from fastapi import UploadFile, File, Request,FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
        # Read image bytes
        contents = await file.read()

        # Convert to base64
        image_base64 = base64.b64encode(contents).decode("utf-8")

        # Simulate POST to internal /extract endpoint
        extract_request = ExtractRequest(image_base64=image_base64)
        response = extract_info(extract_request)

        return JSONResponse(content={"result": response.extracted_fields})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract",response_model=ExtractResponse)
def extract_info(request: ExtractRequest):
    try:
        print("From realdata")
        # Save image from base64
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
            temp_img.write(base64.b64decode(request.image_base64))
            temp_img_path = temp_img.name

        # OCR and clean text
        text = image_to_text(temp_img_path)
        cleaned_text = text.replace("\n", " ").replace("  ", " ")

        # Extraction steps
        regex_output = extract_fields(text)["extracted_fields"]
        ner_output = extract_entities(cleaned_text)
        fallback_output = fallback_extract(cleaned_text)

        # Merge all fields
        final_output = regex_output.copy()
        print("Final:",final_output)
        final_output.update({k: v for k, v in ner_output.items() if v})
        for k, v in fallback_output.items():
            if not final_output.get(k):
                final_output[k] = v
        print("re-check")
        # Fill unknowns and collect missing fields
        required_fields = ["name", "college", "branch", "roll_number", "valid_upto"]
        missing = []
        for field in required_fields:
            if not final_output.get(field):
                final_output[field] = "Unknown"
                missing.append(field)

        # Determine status
        if len(missing) == len(required_fields):
            status = "failure"
        elif missing:
            status = "partial_success"
        else:
            status = "success"

        # Confidence score can be arbitrary for now (you can improve later)
        confidence_score = round(1 - len(missing) / len(required_fields), 2)

        # Derive user_id from OCR or fallback (optional logic)
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


# @app.post("/extract", response_model=ExtractResponse)
# def extract_info(request: ExtractRequest):
#     try:
#         # Save temp image from base64
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img:
#             temp_img.write(base64.b64decode(request.image_base64))
#             temp_img_path = temp_img.name

#         # OCR
#         text = image_to_text(temp_img_path)
#         cleaned_text = text.replace("\n", " ").replace("  ", " ")

#         # Extraction logic
#         regex_output = extract_fields(text)["extracted_fields"]
#         ner_output = extract_entities(cleaned_text)
#         fallback_output = fallback_extract(cleaned_text)

#         # Combine results
#         final_output = regex_output.copy()
#         final_output.update({k: v for k, v in ner_output.items() if v})
#         for k, v in fallback_output.items():
#             if not final_output.get(k):
#                 final_output[k] = v

#         # Fill blanks with "Unknown"
#         for field in ["name", "college", "branch", "roll_number", "valid_upto"]:
#             if not final_output.get(field):
#                 final_output[field] = "Unknown"

#         return ExtractResponse(status="success", extracted_fields=final_output)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))