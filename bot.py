import pyautogui, time, os
import pygetwindow as gw
import pyperclip
from datetime import datetime
import json
from ocr import request_ocr, extract_conversations_by_color, get_dominant_color
from openai import OpenAI

MOUSE_POSITION_DEBUG = False # 마우스 위치 디버깅 여부
NEW_MESSAGE_REGION = (740, 235, 20, 20) # 빨간색 새 메시지 확인 영역 (왼쪽, 위, 너비, 높이)
CONFIDENCE_THRESHOLD = 0.5 # OCR 결과 신뢰도 임계값
DIALOGUE_Y_THRESHOLD = (173, 1036) # 대화 추출 영역 (y좌표, 위, 아래 영역 제거하고 중간 영역만 추출)
CHECK_INTERVAL = 3 # 메시지 확인 주기 (초)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

if MOUSE_POSITION_DEBUG:
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('\n')

while True:
    # 0. 카카오톡 활성화
    gw.getWindowsWithTitle('카카오톡')[0].activate()

    # 1. 새로운 메시지 확인
    img = pyautogui.screenshot(region=NEW_MESSAGE_REGION)
    r, g, b = get_dominant_color(img)

    has_new_message = r > 200 and g < 150 and b < 150
    if not has_new_message:
        time.sleep(3)
        continue

    print(f"[!] 새로운 메시지가 있습니다. {datetime.now()}")

    # 2. 메시지 선택
    pyautogui.click(NEW_MESSAGE_REGION)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    # 3. 활성화된 창 캡처
    active_window = pyautogui.getActiveWindow()

    screenshot = pyautogui.screenshot(region=(
        active_window.left,
        active_window.top,
        active_window.width,
        active_window.height
    ))

    image_path = 'chat_window.png'
    screenshot.save(image_path)

    result = request_ocr(image_path)
    with open('test/result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    # with open('test/result.json', 'r', encoding='utf-8') as f:
    #     result = json.load(f)

    # 3. 대화 추출
    conversations = extract_conversations_by_color(
        result,
        image_path=image_path,
        confidence_threshold=CONFIDENCE_THRESHOLD,
        dialogue_y_threshold=DIALOGUE_Y_THRESHOLD
    )

    logs = []
    for user, message in conversations:
        logs.append(f"{user}: {message}")

    print("[*] 대화 추출")
    print('\n'.join(logs))
    print()

    # 4. 메시지 생성
    messages = [{
        "role": "system",
        "content": "Please provide a response that fits the context based on the following conversation history. Return only the result in Korean without any additional text.\n\n나:"
    }, {
        "role": "user",
        "content": '\n'.join(logs)
    }]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
        max_tokens=1000
    )

    response_message = response.choices[0].message.content
    response_message = response_message.replace('나:', '').strip()
    print("[*] 메시지 생성")
    print(response_message)
    print()

    # 5. 메시지 전송
    pyperclip.copy(response_message)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    # 6. 메시지 전송 후 창 닫기
    pyautogui.hotkey('ctrl', 'w')

    time.sleep(CHECK_INTERVAL)
