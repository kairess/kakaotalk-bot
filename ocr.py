import requests
import uuid
import time
import json
import base64
import os
from PIL import Image

INFER_CONFIDENCE_THRESHOLD = 0.5
DIALOGUE_Y_THRESHOLD = (100, 550)

def request_ocr(image_path):
    api_url = os.getenv('CLOVA_OCR_API_URL')
    secret_key = os.getenv('CLOVA_OCR_SECRET_KEY')

    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo',
                'data': image_data
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': secret_key,
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, headers=headers, data=payload)
    
    return response.json()


def get_dominant_color(image, box=None):
    image = image.convert('RGB')

    if box:
        x1, y1 = box[0]['x'], box[0]['y']
        x2, y2 = box[2]['x'], box[2]['y']
        region = image.crop((x1, y1, x2, y2))
    else:
        region = image

    colors = region.getcolors(region.size[0] * region.size[1])
    return max(colors, key=lambda x: x[0])[1]

def is_yellow(color):
    r, g, b = color
    return r > 200 and g > 200 and b < 100

def is_gray(color):
    r, g, b = color
    return (r > 30 and g > 30 and b > 30) and (r < 60 and g < 60 and b < 60)


def extract_conversations_by_color(ocr_result, image_path, confidence_threshold=0.5, dialogue_y_threshold=(100, 550)):
    image = Image.open(image_path).convert('RGB')
    conversations = []
    current_user = None
    current_message = ""
    
    fields = ocr_result['images'][0]['fields']
    fields.sort(key=lambda x: (x['boundingPoly']['vertices'][0]['y'], x['boundingPoly']['vertices'][0]['x']))
    
    for field in fields:
        if field['inferConfidence'] < confidence_threshold:
            continue

        if field['boundingPoly']['vertices'][0]['y'] < dialogue_y_threshold[0] or field['boundingPoly']['vertices'][3]['y'] > dialogue_y_threshold[1]:
            continue

        text = field['inferText'].strip()
        box = field['boundingPoly']['vertices']
        color = get_dominant_color(image, box)
        
        if is_yellow(color):
            user = "나"
        elif is_gray(color):
            user = "상대방"
        else:
            continue
        
        if current_user != user:
            if current_message:
                conversations.append((current_user, current_message.strip()))
            current_user = user
            current_message = text
        else:
            current_message += " " + text
    
    if current_message:
        conversations.append((current_user, current_message.strip()))
    
    return conversations

if __name__ == "__main__":
    image_path = 'test2.png'

    # result = request_ocr(image_path)
    # with open('result.json', 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)

    with open('result.json', 'r', encoding='utf-8') as f:
        result = json.load(f)

    conversations = extract_conversations_by_color(
        result, 
        image_path,
        confidence_threshold=0.5,
        dialogue_y_threshold=(100, 550)
    )

    for user, message in conversations:
        print(f"{user}: {message}")
