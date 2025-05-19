import streamlit as st
import os
import base64
from typing import Dict, Any, List, Optional
import time

from prompt_templates import PromptTemplates
from claude_api import ClaudeAPI
from document_processor import DocumentProcessor
import config

def main():
    # 앱 설정
    st.set_page_config(
        page_title="법률 문서 작성 도우미",
        page_icon="⚖️",
        layout="wide"
    )
    
    # API 클라이언트 초기화
    if "claude_api" not in st.session_state:
        st.session_state.claude_api = ClaudeAPI()
    
    # 세션 상태 초기화
    if "document_content" not in st.session_state:
        st.session_state.document_content = ""
    if "document_title" not in st.session_state:
        st.session_state.document_title = ""
    if "document_file_path" not in st.session_state:
        st.session_state.document_file_path = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # 앱 헤더
    st.title("⚖️ AI 법률 문서 작성 도우미")
    st.markdown("다양한 법률 문서를 AI의 도움으로 쉽게 작성하세요.")
    
    # 사이드바 - 문서 유형 선택
    st.sidebar.header("문서 설정")
    document_type = st.sidebar.selectbox(
        "문서 유형을 선택하세요",
        list(config.DOCUMENT_TYPES.keys()),
        format_func=lambda x: config.DOCUMENT_TYPES[x]
    )
    
    # 문서 유형별 서브타입 및 추가 옵션
    document_subtype = ""
    if document_type == "litigation":
        document_subtype = st.sidebar.selectbox(
            "소송 문서 유형",
            ["소장", "답변서", "준비서면", "항소장", "상고장", "가처분 신청서"]
        )
    elif document_type == "corporate":
        document_subtype = st.sidebar.selectbox(
            "기업 문서 유형",
            ["이사회 의사록", "주주총회 의사록", "합병계약서", "회사 정관", "사업 제안서"]
        )
    elif document_type == "real_estate":
        document_subtype = st.sidebar.selectbox(
            "부동산 문서 유형",
            ["부동산 매매계약서", "임대차계약서", "부동산 중개 계약서", "부동산 권리 분석서"]
        )
    elif document_type == "ip":
        document_subtype = st.sidebar.selectbox(
            "지식재산권 문서 유형",
            ["특허 라이선스 계약서", "상표 라이선스 계약서", "저작권 양도 계약서", "NDA(비밀유지계약서)"]
        )
    elif document_type == "compliance":
        document_subtype = st.sidebar.selectbox(
            "규제 준수 문서 유형",
            ["내부통제 규정", "개인정보 처리방침", "윤리 강령", "반부패 정책", "공정거래 준수 지침"]
        )
    
    # AI 생성 설정
    st.sidebar.header("AI 생성 설정")
    temperature = st.sidebar.slider("창의성 수준", min_value=0.0, max_value=1.0, value=0.3, step=0.1,
                                  help="낮을수록 일관된 응답, 높을수록 창의적인 응답이 생성됩니다.")
    max_tokens = st.sidebar.slider("최대 토큰 수", min_value=1000, max_value=10000, value=4000, step=1000,
                                 help="생성할 텍스트의 최대 길이입니다.")
    
    # 사용자 입력 양식
    with st.form(key="document_form"):
        st.header(f"{config.DOCUMENT_TYPES[document_type]} 작성")
        
        user_input = get_input_fields(document_type, document_subtype)
        
        # 제출 버튼
        submit_button = st.form_submit_button(label="문서 생성")
    
    # 문서 생성
    if submit_button:
        with st.spinner("문서를 생성 중입니다..."):
            # 시스템 프롬프트 준비
            system_prompt = PromptTemplates.get_system_prompt(document_type)
            
            # 사용자 프롬프트 준비
            user_prompt = PromptTemplates.get_document_template(document_type, user_input)
            
            # API 호출하여 문서 생성
            st.session_state.document_content = st.session_state.claude_api.generate_document(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # 문서 제목 생성
            st.session_state.document_title = DocumentProcessor.get_document_title(document_type, user_input)
            
            # 채팅 기록 업데이트
            st.session_state.chat_history = [
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": st.session_state.document_content}
            ]
    
    # 생성된 문서 표시
    if st.session_state.document_content:
        st.header("생성된 문서")
        
        # 문서 탭과 편집 탭
        tab1, tab2 = st.tabs(["📄 문서 보기", "✏️ 문서 편집"])
        
        with tab1:
            st.subheader(st.session_state.document_title)
            st.markdown(DocumentProcessor.format_document_preview(st.session_state.document_content))
            
            # 문서 다운로드 버튼
            if st.button("Word 문서 생성"):
                with st.spinner("문서 파일을 생성 중입니다..."):
                    docx_file = DocumentProcessor.create_docx(
                        st.session_state.document_content, 
                        st.session_state.document_title
                    )
                    st.session_state.document_file_path = docx_file
            
            if st.session_state.document_file_path:
                with open(st.session_state.document_file_path, "rb") as file:
                    btn = st.download_button(
                        label="Word 문서 다운로드",
                        data=file,
                        file_name=os.path.basename(st.session_state.document_file_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
        
        with tab2:
            # 문서 편집을 위한 채팅 인터페이스
            st.subheader("문서 수정 요청")
            
            revision_prompt = st.text_area("문서 수정 지시사항을 입력하세요:", height=100)
            
            if st.button("수정 요청"):
                with st.spinner("문서를 수정 중입니다..."):
                    # 수정을 위한 새 시스템 프롬프트
                    system_prompt = f"""
{PromptTemplates.get_system_prompt(document_type)}

당신은 법률 문서 편집 전문가입니다. 사용자가 요청한 수정사항을 반영하여 문서를 수정해야 합니다.
원본 문서의 형식과 스타일을 유지하면서 요청된 변경사항만 적용하세요.
수정된 전체 문서를 반환해야 합니다.
"""
                    
                    # 채팅 기록에 새로운 메시지 추가
                    st.session_state.chat_history.append({
                        "role": "user", 
                        "content": f"다음 문서에 대한 수정 요청입니다: {revision_prompt}"
                    })
                    
                    # API 호출하여 수정된 문서 생성
                    response = st.session_state.claude_api.generate_document_with_history(
                        system_prompt=system_prompt,
                        messages=st.session_state.chat_history,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    # 응답 저장 및 표시
                    st.session_state.document_content = response
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                    # 페이지 리프레시를 위해 재실행
                    st.experimental_rerun()
            
            # 채팅 기록 표시
            if len(st.session_state.chat_history) > 2:
                st.subheader("수정 기록")
                for i, msg in enumerate(st.session_state.chat_history[2:], 1):
                    if msg["role"] == "user":
                        st.info(f"요청 {i//2 + i%2}: {msg['content']}")
                    else:
                        st.success(f"수정 {i//2}: 문서가 수정되었습니다.")

def get_input_fields(document_type: str, document_subtype: str = "") -> Dict[str, Any]:
    """문서 유형에 따른 입력 필드 생성"""
    user_input = {}
    
    if document_subtype:
        user_input["document_subtype"] = document_subtype
    
    if document_type == "contract":
        cols = st.columns(2)
        user_input["contract_type"] = cols[0].text_input("계약 종류", "")
        user_input["party_a"] = cols[1].text_input("갑(계약 당사자1)", "")
        user_input["party_b"] = cols[0].text_input("을(계약 당사자2)", "")
        user_input["purpose"] = cols[1].text_input("계약 목적", "")
        user_input["period"] = st.text_input("계약 기간", "")
        user_input["conditions"] = st.text_area("주요 계약 조건", "", height=150)
        user_input["special_requirements"] = st.text_area("특별 요구사항", "", height=100)
        
    elif document_type == "litigation":
        cols = st.columns(2)
        user_input["case_type"] = cols[0].text_input("사건 유형", "")
        user_input["plaintiff"] = cols[1].text_input("원고/신청인", "")
        user_input["defendant"] = cols[0].text_input("피고/피신청인", "")
        user_input["case_summary"] = st.text_area("사건 개요", "", height=150)
        user_input["legal_claims"] = st.text_area("법적 주장 요지", "", height=150)
        user_input["demands"] = st.text_area("청구 내용", "", height=100)
        user_input["evidence"] = st.text_area("관련 증거", "", height=100)
        
    elif document_type == "legal_opinion":
        cols = st.columns(2)
        user_input["client"] = cols[0].text_input("의뢰인", "")
        user_input["legal_question"] = st.text_area("법률 질의 사항", "", height=150)
        user_input["facts"] = st.text_area("관련 사실관계", "", height=150)
        user_input["review_requests"] = st.text_area("검토 요청 사항", "", height=100)
        user_input["applicable_laws"] = st.text_area("적용 법령", "", height=100)
        
    elif document_type == "will":
        cols = st.columns(2)
        user_input["testator"] = cols[0].text_input("유언자 정보", "")
        user_input["will_type"] = cols[1].selectbox(
            "유언장 형식",
            ["자필증서 유언", "공정증서 유언", "비밀증서 유언", "녹음 유언", "구수 유언"]
        )
        user_input["heirs"] = st.text_area("상속인 정보", "", height=100)
        user_input["assets"] = st.text_area("유언 재산 목록", "", height=150)
        user_input["distribution"] = st.text_area("상속 희망 사항", "", height=150)
        user_input["other_wishes"] = st.text_area("기타 유언 사항", "", height=100)
        
    elif document_type == "corporate":
        cols = st.columns(2)
        user_input["company_name"] = cols[0].text_input("회사명", "")
        user_input["related_parties"] = st.text_area("관련 당사자", "", height=100)
        user_input["purpose"] = st.text_area("문서 목적", "", height=100)
        user_input["main_content"] = st.text_area("주요 내용", "", height=200)
        user_input["special_requirements"] = st.text_area("특별 요구사항", "", height=100)
        
    elif document_type == "real_estate":
        cols = st.columns(2)
        user_input["property_type"] = cols[0].text_input("부동산 종류", "")
        user_input["location"] = cols[1].text_input("소재지", "")
        user_input["area"] = cols[0].text_input("면적", "")
        user_input["seller"] = cols[1].text_input("매도인/임대인", "")
        user_input["buyer"] = cols[0].text_input("매수인/임차인", "")
        user_input["price"] = cols[1].text_input("금액", "")
        user_input["payment_terms"] = st.text_area("계약금/중도금/잔금", "", height=100)
        user_input["schedule"] = st.text_area("거래 일정", "", height=100)
        user_input["special_terms"] = st.text_area("특별 약정 사항", "", height=150)
        
    elif document_type == "ip":
        cols = st.columns(2)
        user_input["ip_type"] = cols[0].text_input("지식재산권 유형", "")
        user_input["rights_holder"] = cols[1].text_input("권리자", "")
        user_input["counterparty"] = cols[0].text_input("상대방", "")
        user_input["ip_description"] = st.text_area("권리 내용", "", height=150)
        user_input["purpose"] = st.text_area("계약 목적", "", height=100)
        user_input["usage_terms"] = st.text_area("권리 사용 조건", "", height=150)
        user_input["compensation_period"] = st.text_area("대가 및 기간", "", height=100)
        
    elif document_type == "compliance":
        cols = st.columns(2)
        user_input["organization"] = cols[0].text_input("대상 기업/조직", "")
        user_input["regulatory_area"] = cols[1].text_input("규제 분야", "")
        user_input["applicable_regulations"] = st.text_area("적용 법규", "", height=100)
        user_input["compliance_requirements"] = st.text_area("주요 준수 사항", "", height=150)
        user_input["internal_procedures"] = st.text_area("내부 절차 요구사항", "", height=150)
        user_input["violation_measures"] = st.text_area("위반 시 조치 사항", "", height=100)
    
    return user_input

if __name__ == "__main__":
    main()