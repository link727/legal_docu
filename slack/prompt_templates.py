from typing import Dict, Any
import config

class PromptTemplates:
    """다양한 법률 문서 유형에 대한 프롬프트 템플릿을 관리하는 클래스"""
    
    @staticmethod
    def get_system_prompt(document_type: str) -> str:
        """문서 유형에 따른 시스템 프롬프트 반환"""
        base_prompt = config.DEFAULT_SYSTEM_MESSAGE
        
        type_specific_prompts = {
            "contract": f"""
{base_prompt}

당신은 계약서 작성 전문가입니다. 계약서 작성 시 다음 원칙을 따르세요:
1. 명확한 정의 조항을 포함할 것
2. 계약 당사자들의 권리와 의무를 명시적으로 기술할 것
3. 계약 기간, 종료 조건, 위약금 등 핵심 조항을 포함할 것
4. 준거법과 분쟁 해결 방법을 명시할 것
5. 한국 계약법에 부합하는 내용으로 작성할 것

계약서는 전문적이고 공식적인 어투로 작성하되, 불필요한 법률 용어는 피하고 명확한 표현을 사용하세요.
""",
            "litigation": f"""
{base_prompt}

당신은 소송 문서 작성 전문가입니다. 소송 문서 작성 시 다음 원칙을 따르세요:
1. 사실관계를 객관적이고 명확하게 기술할 것
2. 법적 주장과 그 근거를 논리적으로 전개할 것
3. 관련 법규와 판례를 정확히 인용할 것
4. 청구취지와 청구원인을 명확히 구분하여 기술할 것
5. 한국 민사/형사소송법에 부합하는 형식과 내용으로 작성할 것

소송 문서는 법원과 상대방을 설득할 수 있도록 논리적이고 체계적으로 작성하세요.
""",
            "legal_opinion": f"""
{base_prompt}

당신은 법률 의견서 작성 전문가입니다. 법률 의견서 작성 시 다음 원칙을 따르세요:
1. 질의사항을 명확히 정리하여 제시할 것
2. 관련 법규와 그 해석을 체계적으로 설명할 것
3. 유사 판례와 법률 해석 선례를 참조할 것
4. 구체적인 사안에 대한 법적 분석을 제공할 것
5. 결론과 실무적 권고사항을 명확히 제시할 것

법률 의견서는 전문적이면서도 의뢰인이 이해할 수 있는 수준으로 작성하세요.
""",
            "will": f"""
{base_prompt}

당신은 유언장 작성 전문가입니다. 유언장 작성 시 다음 원칙을 따르세요:
1. 유언자의 인적사항과 유언 의사를 명확히 표현할 것
2. 상속 재산의 구체적인 목록과 분배 방식을 명시할 것
3. 유언 집행자 지정을 포함할 것
4. 한국 민법상 유언의 방식(자필증서, 공정증서 등)에 부합하게 작성할 것
5. 유언의 효력 발생 조건과 시기를 명확히 할 것

유언장은 법적 효력을 갖추면서도 유언자의 의사가 정확히 반영되도록 작성하세요.
""",
            "corporate": f"""
{base_prompt}

당신은 기업 법무 문서 작성 전문가입니다. 기업 법무 문서 작성 시 다음 원칙을 따르세요:
1. 회사법과 상법의 규정에 부합하는 내용으로 작성할 것
2. 이사회 결의, 주주총회 의사록 등 회사 내부 문서의 형식을 준수할 것
3. 기업 지배구조와 의사결정 과정을 명확히 반영할 것
4. 기업의 권리, 의무, 책임 사항을 명확히 기술할 것
5. 관련 규제와 법적 요건을 충족하는 내용으로 작성할 것

기업 법무 문서는 법적 정확성과 비즈니스 실용성을 모두 갖추도록 작성하세요.
""",
            "real_estate": f"""
{base_prompt}

당신은 부동산 관련 법률 문서 작성 전문가입니다. 부동산 문서 작성 시 다음 원칙을 따르세요:
1. 부동산의 정확한 위치, 면적, 특성을 명시할 것
2. 부동산 거래의 조건(매매가, 임대료, 계약기간 등)을 명확히 기술할 것
3. 소유권 이전, 등기, 세금 관련 사항을 포함할 것
4. 부동산 하자 담보책임과 분쟁 해결 방법을 명시할 것
5. 부동산 거래 관련 법규(부동산 거래신고법, 주택임대차보호법 등)를 준수할 것

부동산 문서는 법적 안정성과 거래 당사자 간의 명확한 권리의무 관계를 확보하도록 작성하세요.
""",
            "ip": f"""
{base_prompt}

당신은 지식재산권 관련 법률 문서 작성 전문가입니다. 지식재산권 문서 작성 시 다음 원칙을 따르세요:
1. 지식재산권의 유형(특허, 상표, 저작권 등)을 명확히 구분하여 다룰 것
2. 권리의 내용, 범위, 존속기간을 정확히 기술할 것
3. 권리 침해와 구제수단에 대한 조항을 포함할 것
4. 라이선스, 양도 등 권리 처분 관련 조건을 명확히 할 것
5. 관련 법률(특허법, 상표법, 저작권법 등)의 요건을 충족할 것

지식재산권 문서는 권리자의 이익을 보호하면서도 법적 요건을 충족하도록 작성하세요.
""",
            "compliance": f"""
{base_prompt}

당신은 규제 준수 관련 법률 문서 작성 전문가입니다. 규제 준수 문서 작성 시 다음 원칙을 따르세요:
1. 관련 법규와 규제 요건을 정확히 파악하여 반영할 것
2. 기업의 준수 의무와 절차를 구체적으로 기술할 것
3. 위반 시 제재와 대응 방안을 포함할 것
4. 내부 통제 및 모니터링 시스템에 대한 내용을 포함할 것
5. 최신 법규와 규제 동향을 반영할 것

규제 준수 문서는 법적 리스크를 최소화하고 기업의 지속가능한 운영을 지원하도록 작성하세요.
"""
        }
        
        return type_specific_prompts.get(document_type, base_prompt)
    
    @staticmethod
    def get_document_template(document_type: str, user_input: Dict[str, Any]) -> str:
        """문서 유형과 사용자 입력에 따른 구체적인 프롬프트 템플릿 생성"""
        
        templates = {
            "contract": f"""
다음 정보를 바탕으로 계약서를 작성해주세요:

계약 종류: {user_input.get('contract_type', '일반 계약')}
계약 당사자:
- 갑: {user_input.get('party_a', '')}
- 을: {user_input.get('party_b', '')}
계약 목적: {user_input.get('purpose', '')}
계약 기간: {user_input.get('period', '')}
주요 계약 조건:
{user_input.get('conditions', '')}
특별 요구사항:
{user_input.get('special_requirements', '')}

한국 계약법에 맞게 전문적인 계약서 양식으로 작성해주세요. 모든 필수 조항(계약 목적, 당사자 의무, 계약기간, 대금지급, 계약 위반 시 조치, 분쟁해결 등)을 포함해야 합니다.
""",

            "litigation": f"""
다음 정보를 바탕으로 {user_input.get('document_subtype', '소장')}을 작성해주세요:

사건 유형: {user_input.get('case_type', '')}
당사자 정보:
- 원고/신청인: {user_input.get('plaintiff', '')}
- 피고/피신청인: {user_input.get('defendant', '')}
사건 개요:
{user_input.get('case_summary', '')}
법적 주장 요지:
{user_input.get('legal_claims', '')}
청구 내용:
{user_input.get('demands', '')}
관련 증거:
{user_input.get('evidence', '')}

한국 민사소송법/형사소송법에 맞게 적절한 형식과 내용으로 작성해주세요. 법원에 제출할 수 있는 수준의 완성도를 갖추어야 합니다.
""",

            "legal_opinion": f"""
다음 쟁점에 대한 법률 의견서를 작성해주세요:

의뢰인: {user_input.get('client', '')}
법률 질의 사항:
{user_input.get('legal_question', '')}
관련 사실관계:
{user_input.get('facts', '')}
검토 요청 사항:
{user_input.get('review_requests', '')}
적용 법령:
{user_input.get('applicable_laws', '')}

의견서는 질의사항 정리, 관련 법규 검토, 법적 분석, 결론 및 권고사항의 구조로 작성해주세요.
전문성을 갖추되 의뢰인이 이해할 수 있는 수준으로 설명해주세요.
""",

            "will": f"""
다음 정보를 바탕으로 유언장을 작성해주세요:

유언자 정보: {user_input.get('testator', '')}
상속인 정보:
{user_input.get('heirs', '')}
유언 재산 목록:
{user_input.get('assets', '')}
상속 희망 사항:
{user_input.get('distribution', '')}
기타 유언 사항:
{user_input.get('other_wishes', '')}
유언장 형식: {user_input.get('will_type', '자필증서 유언')}

한국 민법상 유효한 유언장이 될 수 있도록 필요한 모든 법적 요건을 갖추어 작성해주세요.
""",

            "corporate": f"""
다음 정보를 바탕으로 {user_input.get('document_subtype', '이사회 의사록')}을 작성해주세요:

회사명: {user_input.get('company_name', '')}
관련 당사자:
{user_input.get('related_parties', '')}
문서 목적:
{user_input.get('purpose', '')}
주요 내용:
{user_input.get('main_content', '')}
특별 요구사항:
{user_input.get('special_requirements', '')}

한국 상법과 회사법 규정에 맞게 적절한 형식과 내용으로 작성해주세요.
법적 효력을 갖추기 위한 모든 필요 요소를 포함해야 합니다.
""",

            "real_estate": f"""
다음 정보를 바탕으로 {user_input.get('document_subtype', '부동산 매매계약서')}를 작성해주세요:

부동산 정보:
- 종류: {user_input.get('property_type', '')}
- 소재지: {user_input.get('location', '')}
- 면적: {user_input.get('area', '')}
거래 당사자:
- 매도인/임대인: {user_input.get('seller', '')}
- 매수인/임차인: {user_input.get('buyer', '')}
거래 조건:
- 금액: {user_input.get('price', '')}
- 계약금/중도금/잔금: {user_input.get('payment_terms', '')}
- 거래 일정: {user_input.get('schedule', '')}
특별 약정 사항:
{user_input.get('special_terms', '')}

부동산 거래 관련 법규에 맞게 작성하고, 거래의 안전을 보장하는 필요 조항을 모두 포함해주세요.
""",

            "ip": f"""
다음 정보를 바탕으로 {user_input.get('document_subtype', '지식재산권 라이선스 계약서')}를 작성해주세요:

지식재산권 유형: {user_input.get('ip_type', '')}
권리 내용:
{user_input.get('ip_description', '')}
관련 당사자:
- 권리자: {user_input.get('rights_holder', '')}
- 상대방: {user_input.get('counterparty', '')}
계약 목적:
{user_input.get('purpose', '')}
권리 사용 조건:
{user_input.get('usage_terms', '')}
대가 및 기간:
{user_input.get('compensation_period', '')}

관련 지식재산권법에 맞게 작성하고, 권리자의 이익을 보호하면서도 균형 잡힌 계약이 되도록 해주세요.
""",

            "compliance": f"""
다음 정보를 바탕으로 {user_input.get('document_subtype', '내부통제 규정')}을 작성해주세요:

대상 기업/조직: {user_input.get('organization', '')}
규제 분야: {user_input.get('regulatory_area', '')}
적용 법규:
{user_input.get('applicable_regulations', '')}
주요 준수 사항:
{user_input.get('compliance_requirements', '')}
내부 절차 요구사항:
{user_input.get('internal_procedures', '')}
위반 시 조치 사항:
{user_input.get('violation_measures', '')}

관련 법규와 규제 요건을 정확히 반영하고, 실무적으로 적용 가능한 내용으로 작성해주세요.
"""
        }
        
        return templates.get(document_type, "문서 작성에 필요한 정보를 제공해주세요.")