#!/bin/bash

# 스크립트 디렉토리 경로
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 키 파일 경로
KEY_FILE="$SCRIPT_DIR/lightsail.pem"

# IPv4 주소 설정
IPV4="3.39.205.16"

# 디버그 정보 수집
echo "=== IPv4 Connectivity Debug Info ==="
echo "1. Checking local IPv4 configuration..."
ip addr show | grep inet

echo -e "\n2. Checking IPv4 routing..."
ip route

echo -e "\n3. Testing IPv4 connectivity..."
traceroute $IPV4

echo -e "\n4. Checking SSH port..."
nc -zv $IPV4 22

# SSH 연결 시도
echo -e "\n5. Attempting SSH connection..."
ssh -v -i "$KEY_FILE" ubuntu@$IPV4