import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os
import time
from discord import DiscordNotifier


class KoreaInvestmentAPI:
    def __init__(self):
        # .env 파일에서 환경변수 로드
        load_dotenv()

        # 환경변수에서 API 키 가져오기
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API_KEY와 API_SECRET이 .env 파일에 설정되어 있지 않습니다."
            )

        self.base_url = "https://openapi.koreainvestment.com:9443"

        # 토큰 파일 경로
        self.token_file = "token.json"

        # 토큰 가져오기 (저장된 토큰이 없거나 만료된 경우 새로 발급)
        self.access_token = self._load_or_get_token()

    def _load_or_get_token(self):
        """저장된 토큰을 불러오거나 새로운 토큰을 발급받음"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, "r") as f:
                    token_data = json.load(f)

                # 토큰 만료 시간 확인
                expires_at = datetime.strptime(
                    token_data["expires_at"], "%Y-%m-%d %H:%M:%S"
                )
                if datetime.now() < expires_at:
                    print("Using cached token")
                    return token_data["access_token"]

                print("Cached token expired, getting new token")

            # 새로운 토큰 발급
            return self._get_new_token()

        except Exception as e:
            print(f"Error loading token: {e}")
            return self._get_new_token()

    def _get_new_token(self):
        """새로운 토큰 발급"""
        url = f"{self.base_url}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "appsecret": self.api_secret,
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))
        response_data = response.json()

        # 토큰 정보 저장
        token_data = {
            "access_token": response_data["access_token"],
            "expires_at": response_data["access_token_token_expired"],
        }

        # 토큰을 파일에 저장
        with open(self.token_file, "w") as f:
            json.dump(token_data, f)

        print("New token generated and saved")
        return response_data["access_token"]

    def get_trading_volume_rank(self):
        """거래량 순위 조회 (당일)"""
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/volume-rank"

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.api_key,
            "appsecret": self.api_secret,
            "tr_id": "FHPST01710000",
            "custtype": "P",
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_COND_SCR_DIV_CODE": "20171",
            "FID_INPUT_ISCD": "0002",
            "FID_DIV_CLS_CODE": "0",
            "FID_BLNG_CLS_CODE": "0",
            "FID_TRGT_CLS_CODE": "111111111",
            "FID_TRGT_EXLS_CLS_CODE": "000000",
            "FID_INPUT_PRICE_1": "0",
            "FID_INPUT_PRICE_2": "0",
            "FID_VOL_CNT": "0",
            "FID_INPUT_DATE_1": "0",
        }

        # 요청 파라미터 로깅
        print("\n=== API Request Parameters ===")
        print("Parameters:", json.dumps(params, indent=2))

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def format_ranking_data(self, data):
        """거래대금 순위 데이터 포맷팅"""
        # API 응답 구조 확인을 위한 디버깅
        print("Data structure:", data.keys())

        if "output" not in data:
            raise ValueError(
                f"Unexpected API response format. Available keys: {data.keys()}"
            )

        records = data["output"]
        df = pd.DataFrame(records)

        # 실제 컬럼 확인을 위한 디버깅
        print("Actual columns:", list(df.columns))

        # API 응답의 실제 컬럼에 맞춰 수정된 컬럼명 매핑
        column_mapping = {
            "stck_shrn_iscd": "종목코드",
            "stck_prpr": "현재가",
            "prdy_vrss_sign": "전일대비구분",
            "prdy_vrss": "전일대비",
            "prdy_ctrt": "등락율",
            "acml_vol": "거래량",
            "acml_tr_pbmn": "거래대금",
            "stck_oprc": "시가",
            "stck_hgpr": "고가",
            "stck_lwpr": "저가",
            "hts_kor_isnm": "종목명",
            "stck_mktc": "시가총액",
            "lstn_stcn": "상장주식수",
            "fprc": "외국인보유비율",
            "pgtr": "PER",
            "eps": "EPS",
            "pbr": "PBR",
            "bps": "BPS",
        }

        # 컬럼명 변경
        df = df.rename(columns=column_mapping)

        # 숫자형 데이터 변환
        numeric_columns = [
            "현재가",
            "전일대비",
            "등락율",
            "거래량",
            "거래대금",
            "시가",
            "고가",
            "저가",
            "시가총액",
            "상장주식수",
            "외국인보유비율",
            "PER",
            "EPS",
            "PBR",
            "BPS",
        ]

        for col in numeric_columns:
            if col in df.columns:  # 컬럼이 존재
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # 거래대금 단위를 억원으로 변환
        df["거래대금"] = (df["거래대금"] / 100000000).round(2)

        return df


class StockConfig:
    # 표시할 컬럼 설정
    DISPLAY_COLUMNS = {
        "종목명": "hts_kor_isnm",
        "현재가": "stck_prpr",
        "등락율": "prdy_ctrt",
        "거래대금": "acml_tr_pbmn",
    }

    # API 관련 설정
    API_CONFIG = {
        "market": "KOSPI",  # KOSPI or KOSDAQ
        "rank_type": "volume",  # volume, price, etc
        "limit": 50,
    }


class StockDataProcessor:
    def __init__(self, api):
        self.api = api

    def get_week_dates(self):
        """이번주의 거래일 목록 생성"""
        today = datetime.now()
        # 오늘이 월요일인 경우를 찾아서 시작일 계산
        monday = today - timedelta(days=today.weekday())

        # 주중 날짜 리스트 생성 (월~금)
        dates = []
        for i in range(5):  # 0=월요일, 4=금요일
            date = monday + timedelta(days=i)
            # 미래 날짜는 제외
            if date <= today:
                dates.append(date.strftime("%Y%m%d"))
        return dates

    def collect_weekly_data(self):
        """한 주 데이터 수집"""
        dates = self.get_week_dates()
        weekly_data = []

        for date in dates:
            try:
                print(f"\n{date} 데이터 수집 시작...")
                ranking_data = self.api.get_trading_volume_rank(target_date=date)

                # 데이터 유효성 검증
                if not ranking_data or "output" not in ranking_data:
                    print(f"{date} 데이터 형식 오류")
                    continue

                df = self.api.format_ranking_data(ranking_data)

                # 데이터 검증
                if df.empty:
                    print(f"{date} 데이터 없음")
                    continue

                df["조회일자"] = date

                # 데이터 검증 출력
                print(f"수집된 종목 수: {len(df)}")
                print(f"첫 번째 종목: {df.iloc[0]['종목명']} - {df.iloc[0]['현재가']}")

                weekly_data.append(df)

                # API 호출 간격 조절
                time.sleep(1)

            except Exception as e:
                print(f"{date} 데이터 수집 실패: {e}")

        # 모든 데이터 합치기
        if weekly_data:
            combined_df = pd.concat(weekly_data, ignore_index=True)
            return combined_df
        return None

    def save_to_csv(self, df, filename=None):
        """데이터프레임을 CSV로 저장"""
        if filename is None:
            today = datetime.now().strftime("%Y%m%d")
            filename = f"stock_ranking_week_{today}.csv"

        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"데이터가 {filename}로 저장되었습니다.")


class StockDisplayManager:
    @staticmethod
    def display_ranking(df):
        """순위 데이터 출력"""
        print("\n=== 이번주 거래대금 상위 30종목 ===")
        print(df.to_string(index=True))

    @staticmethod
    def display_error(error_msg):
        """에러 메시지 출력"""
        print(f"Error: {error_msg}")


def main():
    try:
        # Discord 알림 객체 생성
        discord = DiscordNotifier()

        # API 초기화
        api = KoreaInvestmentAPI()

        # 당일 데이터 수집
        data = api.get_trading_volume_rank()
        df = api.format_ranking_data(data)

        if df is not None:
            # 현재 날짜를 파일명에 포함
            today = datetime.now().strftime("%Y%m%d")
            filename = f"stock_ranking_{today}.csv"
            df.to_csv(filename, index=False, encoding="utf-8")

            # Discord로 알림 전송
            discord.send_notification(df, filename)

            # 결과 출력
            print("\n=== 거래대금 상위 종목 요약 ===")
            summary_columns = ["종목명", "현재가", "등락율", "거래대금"]
            print(df[summary_columns].to_string(index=False))
            print(f"\n데이터가 {filename}에 저장되었습니다.")

        else:
            print("수집된 데이터가 없습니다.")
            discord.send_error_notification("데이터 수집 실패")

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        # 에러 발생 시 Discord로 알림
        discord.send_error_notification(error_msg)


if __name__ == "__main__":
    main()
