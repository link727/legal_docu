# Legal Document AI Generator

이 프로젝트는 Streamlit, Python, Claude API를 사용하여
다양한 법률 문서를 작성하는 AI임.

## 기능

- 8가지 법률 문서 유형 지원 
(계약서, 소송 문서, 법률 의견서, 유언장, 기업 법무 문서, 
부동산 관련 문서, 지식재산권 문서, 규제 준수 문서)
- 문서 유형별 특화된 프롬프트 템플릿
- 사용자 정보에 기반한 문서 자동 생성
- 생성된 문서 편집 및 수정
- Word 문서 다운로드 기능

## 시스템 아키텍처

시스템은 다음과 같은 구성요소로 이루어져 있습니다:

1. **사용자 인터페이스 (app.py)**: Streamlit 기반 웹 인터페이스
2. **프롬프트 관리 시스템 (prompt_templates.py)**: 문서 유형별 프롬프트 템플릿
3. **API 연동 시스템 (claude_api.py)**: Claude API와 통신
4. **문서 처리 시스템 (document_processor.py)**: 문서 생성 및 변환
5. **설정 관리 (config.py)**: 시스템 설정

## 설치 및 실행 방법

1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

2. API 키 설정
```bash
# .env 파일 생성
echo "-" > .env
echo "CLAUDE_MODEL=claude-3-5-sonnet-20241022" >> .env
```
3. 애플리케이션 실행
```bash
streamlit run app.py
```

## 사용 방법

1. 사이드바에서 문서 유형 선택
2. 필요한 정보 입력
3. "문서 생성" 버튼 클릭
4. 생성된 문서 확인
5. 필요시 문서 수정 요청
6. Word 문서로 다운로드

## 파일 구조

- **app.py**: 메인 애플리케이션 파일
- **prompt_templates.py**: 프롬프트 템플릿 관리
- **claude_api.py**: Claude API 래퍼
- **document_processor.py**: 문서 처리 유틸리티
- **config.py**: 설정 파일
- **requirements.txt**: 필요 패키지 목록
- **temp/**: 임시 파일 저장 디렉토리

## 확장 방법

새로운 문서 유형을 추가하려면:

1. `config.py`의 `DOCUMENT_TYPES` 딕셔너리에 새 유형 추가
2. `prompt_templates.py`에 새 문서 유형의 시스템 프롬프트와 템플릿 추가
3. `app.py`의 `get_input_fields()` 함수에 새 문서 유형의 입력 필드 추가
4. `document_processor.py`의 `get_document_title()` 함수에 새 문서 유형의 제목 생성 로직 추가