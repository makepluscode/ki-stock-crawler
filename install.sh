#!/bin/bash

# 가상환경 디렉토리 이름
VENV_NAME="venv"

# 가상환경이 없으면 생성
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_NAME
fi

# 가상환경 활성화
source $VENV_NAME/bin/activate

# requirements.txt 생성 (처음 한 번만 필요)
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    echo "requests==2.31.0" > requirements.txt
    echo "pandas==2.2.1" >> requirements.txt
fi

# 필요한 패키지 설치
echo "Installing required packages..."
pip install -r requirements.txt

# 가상환경 비활성화
deactivate