import pyautogui, time, sys
from datetime import datetime
from ocr import extract_conversations_by_color, get_dominant_color

MOUSE_POSITION_DEBUG = False

NEW_MESSAGE_REGION = (535, 120, 15, 15)


def check_new_message():
    img = pyautogui.screenshot(region=NEW_MESSAGE_REGION)
    r, g, b = get_dominant_color(img)
    if r > 200:
        return True
    return False


if __name__ == "__main__":
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
        pyautogui.click(NEW_MESSAGE_REGION)

        # 1. 새로운 메시지 확인
        if check_new_message():
            print(f"[!] 새로운 메시지가 있습니다. {datetime.now()}")

            # 2. 메시지 선택
            pyautogui.click(NEW_MESSAGE_REGION)
            time.sleep(1)
            # pyautogui.press('enter')
            # time.sleep(1)

        # 3. 활성화된 창 캡처
        # Windows 코드는 변경 없음
        active_window = pyautogui.getActiveWindow()
        screenshot = pyautogui.screenshot(region=(
            active_window.left,
            active_window.top,
            active_window.width,
            active_window.height
        ))

        # 디버깅을 위해 스크린샷을 저장하고 경로를 출력합니다
        screenshot_path = 'active_window_screenshot.png'
        screenshot.save(screenshot_path)
        print(f"활성화된 창의 스크린샷이 {screenshot_path}에 저장되었습니다.")
        break

        # 3. Extract conversations
        conversations = extract_conversations_by_color()

        # 4. Send message
        send_message(conversations)
