import anthropic
from typing import Dict, Any, List, Optional
import config

class ClaudeAPI:
    """Claude API와 통신하는 래퍼 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        """API 클라이언트 초기화"""
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        self.client = anthropic.Client(api_key=self.api_key)  # 올바른 Client 객체 생성
        self.model = config.CLAUDE_MODEL
    
    def generate_document(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Claude API를 호출하여 문서 생성"""
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API 호출 중 오류 발생: {e}")
            return f"문서 생성 중 오류가 발생했습니다: {str(e)}"
    
    def generate_document_with_history(
        self,
        system_prompt: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """대화 기록을 포함하여 Claude API 호출"""
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API 호출 중 오류 발생: {e}")
            return f"문서 생성 중 오류가 발생했습니다: {str(e)}"