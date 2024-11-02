#!/bin/bash

# 스크립트 경로 가져오기
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 임시 crontab 파일 생성
TEMP_CRON=$(mktemp)

# 기존 crontab 내용 보존
crontab -l > "$TEMP_CRON" 2>/dev/null

# 기존 stock data 수집 작업이 있다면 제거
sed -i '/stock_data.*run.sh/d' "$TEMP_CRON"

# 새로운 cron 작업 추가 (평일 15:40에 실행)
echo "40 15 * * 1-5 $SCRIPT_DIR/run.sh" >> "$TEMP_CRON"

# 새로운 crontab 설정 적용
crontab "$TEMP_CRON"

# 임시 파일 삭제
rm "$TEMP_CRON"

# 설정 확인
echo "Current crontab settings:"
crontab -l

echo "Crontab setup completed!" 