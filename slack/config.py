import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키 설정
ANTHROPIC_API_KEY = os.getenv("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")

# Claude 모델 설정
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

# 문서 유형 정의
DOCUMENT_TYPES = {
    "contract": "계약서",
    "litigation": "소송 문서",
    "legal_opinion": "법률 의견서",
    "will": "유언장",
    "corporate": "기업 법무 문서",
    "real_estate": "부동산 관련 문서",
    "ip": "지식재산권 문서",
    "compliance": "규제 준수 문서"
}

# 기본 시스템 메시지
DEFAULT_SYSTEM_MESSAGE = """법률 전문가로서 정확하고 전문적인 법률 문서를 작성하는 역할을 수행합니다. 
문서는 한국 법률과 관행에 따라 작성되어야 하며, 전문 용어를 적절히 사용하고,
논리적이고 명확한 문장 구조를 유지해야 합니다. 
최신 법률과 판례를 반영하되, 구체적인 법조항을 인용할 때는 정확성을 확보해야 합니다."""

# 임시 파일 저장 경로
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)