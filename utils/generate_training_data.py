import os 
import json 
import re 
from model.ocr import image_to_text

def get_training_data(images_dir="/dataset/images",labels_dir="dataset/labels"):
    training_data=[]
    for filename in os.listdir(labels_dir):
        if filename.endswith(".json"):
            label_path=os.path.join(labels_dir,filename)
            filename=filename.replace(".json",".png")
            image_path = os.path.join("dataset", "images", filename)
            print("🔍 Loading image:", image_path)
            
            with open(label_path , "r")as f:
                label=json.load(f)
                
            raw_text=image_to_text(image_path)
            
            entities=[]
            
            for field in ["name","college","branch"]:
                value=label["extracted_fields"].get(field)
                if value:
                    match=re.search(re.escape(value),raw_text)
                    if match:
                        entities.append((match.start(),match.end(),field.upper()))
                
            training_data.append((raw_text,{"entities":entities}))
            
    return training_data
                