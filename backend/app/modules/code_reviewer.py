"""Code Review module."""
import logging
from typing import Dict, Any, List

from app.connectors import ChatMessage
from app.connectors.factory import get_connector

logger = logging.getLogger(__name__)

class CodeReviewer:
    """Performs code analysis and review."""
    
    def __init__(self):
        """Initialize the code reviewer."""
        self.connector = get_connector()
    
    async def review_code(
        self,
        code: str,
        language: str = "python",
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Perform code review on provided code.
        
        Args:
            code: Code to review
            language: Programming language
            context: Additional context about the code
            
        Returns:
            Review results with findings and suggestions
        """
        try:
            prompt = self._build_review_prompt(code, language, context)
            messages = [
                ChatMessage(
                    role="system",
                    content="You are an expert code reviewer. Analyze code for quality, security, performance, and best practices."
                ),
                ChatMessage(role="user", content=prompt)
            ]
            
            response = await self.connector.send_chat(messages)
            
            return {
                "success": True,
                "code_language": language,
                "review": response,
                "code_length": len(code),
            }
        except Exception as e:
            logger.error(f"Code review failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_review_prompt(self, code: str, language: str, context: str) -> str:
        """Build the review prompt."""
        prompt = f"""Please review the following {language} code and provide structured feedback.

Context: {context if context else "No additional context provided"}

Code to review:
```{language}
{code}
```

Please provide feedback on:
1. Code Quality and Style
2. Potential Bugs and Issues
3. Performance Considerations
4. Security Issues
5. Best Practices
6. Suggestions for Improvement

Format your response as a structured report."""
        return prompt
