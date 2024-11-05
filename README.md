# Korea Investment Crawler

한국투자증권 API를 활용한 주식 시장 데이터 수집 도구입니다.

## 개요

이 프로젝트는 한국투자증권의 Open API를 활용하여 주식 시장 데이터를 자동으로 수집하고 분석하는 도구입니다. 실시간 시세, 거래량, 호가 정보 등을 수집하여 CSV 형태로 저장하고 분석할 수 있습니다.

## 주요 기능

- 실시간 거래량 순위 데이터 수집
- 일별/주별 거래 데이터 저장
- CSV 형식으로 데이터 내보내기
- 자동 토큰 관리 (만료 시 자동 갱신)
- 실시간 호가 정보 수집
- 거래량 급증 종목 알림

## 시작하기

### 필수 조건

- Python 3.8 이상
- 한국투자증권 API 키 (앱 키와 시크릿)
- 필수 Python 패키지:
  - requests
  - pandas
  - python-dotenv

### 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/your-username/ki-stock-crawler.git
cd ki-stock-crawler
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어 API_KEY와 API_SECRET 입력
```

### Discord 알림 설정

1. Discord 웹훅 URL 얻기
   - Discord 서버 설정 → 연동 → 웹후크
   - '새 웹후크' 생성
   - 웹후크 이름 설정 (예: "Stock Bot")
   - 채널 선택
   - '웹후크 URL 복사' 클릭

2. 환경 변수에 웹훅 URL 추가
```bash
# .env 파일에 추가
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

3. 알림 기능
   - 거래대금 상위 10종목 정보
   - CSV 파일 자동 첨부
   - 에러 발생 시 자동 알림
   - 매 시간 정각 실행 결과 통보

### 실행 방법


## 데이터 형식

수집되는 데이터는 다음 필드를 포함합니다:
- 종목코드
- 종목명
- 현재가
- 거래량
- 거래대금
- 등락률
- 시가총액
- 시가/고가/저가

## 프로젝트 구조

```
korea-investment-crawler/
├── app.py                 # 메인 실행 파일
├── crawler/
│   ├── __init__.py
│   ├── api.py            # API 연동 모듈
│   └── utils.py          # 유틸리티 함수
├── discord.py           # Discord 알림 모듈
├── data/                # 데이터 저장 디렉토리
├── requirements.txt     # 의존성 패키지 목록
├── .env.example        # 환경 변수 예시 파일
├── .gitignore          # Git 무시 파일 목록
└── README.md           # 프로젝트 문서
```

## 주의사항

- API 호출 횟수 제한을 준수해주세요
- 실제 투자에 사용 시 충분한 검증이 필요합니다
- 키 파일과 인증 정보를 안전하게 관리해주세요

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
