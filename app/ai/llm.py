# File: app/ai/llm.py
"""
Groq LLM wrapper using LangChain.
"""
from typing import Optional, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.LLM")

# Global LLM instance
_llm: Optional[ChatGroq] = None


def get_llm() -> ChatGroq:
    """Get or create the Groq LLM instance."""
    global _llm
    
    if _llm is None:
        logger.info(f"Initializing Groq LLM with model: {settings.GROQ_MODEL}")
        
        _llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.7,
            max_tokens=4096,
        )
        
        logger.info("Groq LLM initialized successfully.")
    
    return _llm


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> str:
    """
    Generate text using the LLM.
    
    Args:
        prompt: The user prompt
        system_prompt: Optional system prompt for context
        temperature: Creativity setting (0-1)
        max_tokens: Maximum tokens in response
    
    Returns:
        Generated text
    """
    llm = get_llm()
    
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=prompt))
    
    try:
        response = await llm.ainvoke(messages)
        return response.content
    except Exception as e:
        logger.error(f"LLM generation error: {str(e)}")
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_json(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.5
) -> Dict[str, Any]:
    """
    Generate structured JSON output using the LLM.
    
    Args:
        prompt: The user prompt requesting JSON output
        system_prompt: Optional system prompt
        temperature: Creativity setting (lower for more consistent JSON)
    
    Returns:
        Parsed JSON dictionary
    """
    llm = get_llm()
    parser = JsonOutputParser()
    
    # Add JSON instruction to system prompt
    json_instruction = "\n\nYou must respond with valid JSON only. No markdown, no explanations, just the JSON object."
    
    full_system = (system_prompt or "") + json_instruction
    
    messages = [
        SystemMessage(content=full_system),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = await llm.ainvoke(messages)
        content = response.content
        
        # Clean up any markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return parser.parse(content.strip())
    except Exception as e:
        logger.error(f"LLM JSON generation error: {str(e)}")
        raise


async def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.
    Rough approximation: ~4 characters per token.
    """
    return len(text) // 4
