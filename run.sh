#!/bin/bash

# 스크립트 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR

# 로그 디렉토리 생성
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p $LOG_DIR

# 로그 파일 설정
LOG_FILE="$LOG_DIR/stock_log_$(date '+%Y%m%d').log"

# 가상환경 활성화
source venv/bin/activate

# 실행 시작 로그
echo "=== Stock Data Collection Started at $(date) ===" >> "$LOG_FILE"

# Python 스크립트 실행
python app.py >> "$LOG_FILE" 2>&1

# 실행 완료 로그
echo "=== Completed at $(date) ===" >> "$LOG_FILE"

# 가상환경 비활성화
deactivate

# 30일 이상된 로그 삭제
find "$LOG_DIR" -name "stock_log_*.log" -mtime +30 -exec rm {} \;