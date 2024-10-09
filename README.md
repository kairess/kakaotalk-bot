# 카카오톡 자동 응답 봇

이 프로젝트는 카카오톡 메시지를 자동으로 감지하고 응답하는 봇입니다. OpenAI의 GPT 모델을 사용하여 대화 맥락에 맞는 응답을 생성합니다.

|  |  |  |
| --- | --- | --- |
| ![](result/0.jpg) | ![](result/1.jpg) | ![](result/2.jpg) |

## 주요 기능

- 새로운 카카오톡 메시지 감지
- 대화창 캡처 및 OCR을 통한 텍스트 추출
- GPT 모델을 사용한 맥락에 맞는 응답 생성
- 자동 응답 전송

## 필요 조건

- Python 3.7+
- 필요한 라이브러리: pyautogui, pygetwindow, pyperclip, openai
- OpenAI API 키

## 설치 방법

1. 저장소를 클론합니다:
   ```
   git clone https://github.com/kairess/kakaotalk-bot.git
   ```

2. 필요한 라이브러리를 설치합니다:
   ```
   pip install pyautogui pygetwindow pyperclip openai
   ```

3. OpenAI API 키를 환경 변수로 설정합니다:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## 사용 방법

1. 카카오톡 PC 버전을 실행하고 로그인합니다.

2. 스크립트를 실행합니다:
   ```
   python bot.py
   ```

3. 스크립트가 실행되면 새로운 카카오톡 메시지를 자동으로 감지하고 응답합니다.

## 주의사항

- Windows 환경에서 실행해야 합니다. (맥, 리눅스 환경에서는 불가)
- 이 봇은 개인적인 용도로만 사용해야 합니다.
- 과도한 사용은 카카오톡 서비스 약관을 위반할 수 있습니다.
- OpenAI API 사용에 따른 비용이 발생할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
