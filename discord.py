import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import logging

class DiscordNotifier:
    """Discord 웹훅을 통해 알림을 보내는 클래스"""
    
    def __init__(self):
        """Discord 웹훅 URL 초기화 및 로깅 설정"""
        # 환경변수 로드
        load_dotenv()
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        # 웹훅 URL 검증
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL이 .env 파일에 설정되어 있지 않습니다.")
            
        # 로깅 설정
        self._setup_logging()
        
        # 기본 설정
        self.BOT_NAME = "Stock Bot"
        self.BOT_AVATAR = "https://i.imgur.com/4M34hi2.png"
        self.ERROR_BOT_NAME = "Stock Bot Error"
    
    def _setup_logging(self) -> None:
        """로깅 설정"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_table_header(self) -> str:
        """테이블 헤더 생성"""
        return (f"{'종목명':<10} {'현재가':>8} {'등락률':>7} {'거래대금':>10}\n"
                + "-" * 40 + "\n")
    
    def _format_row(self, row: pd.Series) -> str:
        """데이터 행 포맷팅"""
        return (f"{row['종목명']:<10} {row['현재가']:>8,} "
                f"{row['등락율']:>6.1f}% {row['거래대금']:>9.0f}억\n")
    
    def format_message(self, df: pd.DataFrame) -> str:
        """DataFrame을 Discord 메시지 형식으로 변환"""
        try:
            # 상위 10개 종목 선택
            top_10 = df.head(10)
            
            # 메시지 구성
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            message_parts = [
                "📊 **오늘의 거래대금 상위 10종목**",
                f"_{current_time} 기준_\n",
                "```",
                self._create_table_header(),
                "".join(self._format_row(row) for _, row in top_10.iterrows()),
                "```"
            ]
            
            return "\n".join(message_parts)
            
        except Exception as e:
            self.logger.error(f"메시지 포맷팅 중 오류 발생: {str(e)}")
            raise
    
    def _prepare_payload(self, message: str, is_error: bool = False) -> Dict[str, Any]:
        """Discord webhook 페이로드 준비"""
        return {
            "content": message,
            "username": self.ERROR_BOT_NAME if is_error else self.BOT_NAME,
            "avatar_url": self.BOT_AVATAR
        }
    
    def _send_webhook(self, payload: Dict[str, Any], files: Optional[Dict] = None) -> None:
        """Discord webhook 요청 전송"""
        response = requests.post(
            self.webhook_url,
            data=payload if files else None,
            json=payload if not files else None,
            files=files
        )
        
        # 200과 204 모두 성공으로 처리
        if response.status_code not in [200, 204]:
            raise requests.RequestException(
                f"Discord webhook 요청 실패: {response.status_code}"
            )
    
    def send_notification(self, df: pd.DataFrame, file_path: Optional[str] = None) -> None:
        """Discord로 알림 전송"""
        try:
            # 메시지 생성
            message = self.format_message(df)
            payload = self._prepare_payload(message)
            
            # 파일 첨부 준비
            files = None
            if file_path and os.path.exists(file_path):
                files = {
                    'file': (
                        os.path.basename(file_path),
                        open(file_path, 'rb'),
                        'text/csv'
                    )
                }
            
            # webhook 전송
            self._send_webhook(payload, files)
            self.logger.info("Discord 알림 전송 성공!")
            
        except Exception as e:
            self.logger.error(f"Discord 알림 전송 중 오류 발생: {str(e)}")
            raise
        finally:
            # 파일 핸들러 정리
            if files:
                files['file'][1].close()
    
    def send_error_notification(self, error_message: str) -> None:
        """에러 발생 시 Discord로 알림 전송"""
        try:
            message = f"⚠️ **에러 발생**\n```\n{error_message}\n```"
            payload = self._prepare_payload(message, is_error=True)
            
            self._send_webhook(payload)
            self.logger.info("Discord 에러 알림 전송 성공!")
            
        except Exception as e:
            self.logger.error(f"Discord 에러 알림 전송 중 오류 발생: {str(e)}")
            raise 