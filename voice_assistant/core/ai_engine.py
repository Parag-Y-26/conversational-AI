"""
AI Engine - Kimi K2.5 via Ollama Cloud
Implements Blue Machine AI-style conversation rules:
- No chain of thought/reasoning - direct answers only
- Contextual continuity across conversation
- Fast, concise responses for voice
- Hallucination resistance - factual grounded responses
- Compliance under pressure - avoids speculation
"""
import httpx
import re
from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
import asyncio

# Ollama Cloud Configuration
OLLAMA_API_KEY = "cd826e7a76244edebdf1ba1802410746.8hLndyNjWNmOKkpRBkJ1Vqpl"
OLLAMA_BASE_URL = "https://ollama.com/api"
OLLAMA_MODEL = "kimi-k2.5"

class AIProvider(Enum):
    OLLAMA = "ollama"

@dataclass
class Message:
    role: str
    content: str

@dataclass
class AIResponse:
    content: str
    provider: AIProvider
    model: str
    success: bool
    error: Optional[str] = None

class AIEngine:
    """
    AI Engine with Blue Machine AI-style conversation rules:
    - Direct answers only - no thinking/reasoning output
    - Contextual memory across conversation
    - Fast voice-optimized responses (1-2 sentences)
    - Grounded factual responses
    """
    
    def __init__(self, timeout: float = 30.0, **kwargs):
        self.timeout = timeout
        self.history: List[Message] = []
        self.max_history = 20  # Longer context for continuity
        
        # Blue Machine AI-inspired system prompt
        self.system_prompt = """You are Nebula, an advanced voice assistant.

CRITICAL RULES:
1. OUTPUT ONLY YOUR FINAL ANSWER - never show thinking, reasoning, or drafts
2. Keep responses to 1-2 sentences (will be spoken aloud)
3. Be direct, natural, and conversational
4. Stay factual - if unsure, say so honestly
5. Never speculate or make claims you can't verify
6. Maintain context from previous conversation
7. Use plain speech - no markdown, asterisks, or formatting

RESPOND TO THE USER DIRECTLY. NO EXPLANATIONS OF WHAT YOU'RE DOING."""
        
        self._client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)
        print(f"[AI] Using Ollama Cloud ({OLLAMA_MODEL})")
    
    def _extract_final_answer(self, text: str) -> str:
        """Extract only the final spoken answer - remove ALL reasoning"""
        if not text:
            return "I'm here to help!"
        
        # First check for quoted final response
        quotes = re.findall(r'"([^"]{5,100})"', text)
        if quotes:
            return quotes[-1].strip()
        
        # Remove all thinking/reasoning patterns aggressively
        thinking_patterns = [
            r"(?i)(I think|I should|Let me|I need|I'll|I will|Since|Given|The user|Draft|Option|Approach|Constraint|Rule|Step|First|Wait|Hmm|Ok so|So I|My response|I'm going to|thinking|reasoning|considering).*?(?=\n|$)",
            r"^\d+\.\s*.*$",  # Numbered items
            r"^[-*]\s*.*$",   # Bullet points
            r"^[A-Z][a-z]+:.*$",  # Labels like "Response:"
        ]
        
        # Split into lines and filter
        lines = text.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that look like thinking
            is_thinking = False
            for pattern in thinking_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    is_thinking = True
                    break
            
            if not is_thinking:
                # Additional checks
                lower = line.lower()
                skip_starts = ('i think', 'i should', 'let me', 'since', 'given', 
                              'the user', 'draft', 'option', 'so i', 'i need',
                              'i\'ll', 'wait', 'hmm', 'ok', 'step', 'first',
                              'constraint', 'rule', 'approach', 'my response')
                if not any(lower.startswith(s) for s in skip_starts):
                    clean_lines.append(line)
        
        if clean_lines:
            # Return the first clean line that looks like an answer
            for line in clean_lines:
                if len(line) > 3 and not line.endswith(':'):
                    text = line
                    break
            else:
                text = clean_lines[0]
        
        # Final cleanup
        text = re.sub(r'\*+', '', text)  # Remove asterisks
        text = re.sub(r'#+', '', text)   # Remove hashtags
        text = text.strip().strip('"\'')
        
        # Limit length for voice
        if len(text) > 200:
            # Cut at sentence boundary
            sentences = re.split(r'(?<=[.!?])\s+', text)
            text = ' '.join(sentences[:2])
        
        return text if text else "I'm here to help!"
    
    def _build_messages(self, user_input: str, screen_context: Optional[str] = None) -> List[Dict]:
        """Build message list with contextual history"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history for contextual continuity
        for msg in self.history[-self.max_history:]:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Current user input
        if screen_context:
            user_content = f"[Screen context: {screen_context[:200]}]\n{user_input}"
        else:
            user_content = user_input
        
        messages.append({"role": "user", "content": user_content})
        return messages
    
    async def get_response(
        self,
        user_input: str,
        screen_context: Optional[str] = None,
        use_fallback: bool = True
    ) -> AIResponse:
        """Get AI response - returns clean, direct answer only"""
        messages = self._build_messages(user_input, screen_context)
        
        try:
            print(f"[AI] Calling Ollama ({OLLAMA_MODEL})...")
            
            response = await self._client.post(
                f"{OLLAMA_BASE_URL}/chat",
                headers={
                    "Authorization": f"Bearer {OLLAMA_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OLLAMA_MODEL,
                    "messages": messages,
                    "stream": False,
                    "think": False,  # Disable chain-of-thought output
                    "options": {
                        "num_predict": 300,  # Allow complete answers
                        "temperature": 0.7
                    }
                }
            )
            
            if response.status_code == 404:
                print("[AI] Trying /generate endpoint...")
                prompt = f"{self.system_prompt}\n\nUser: {user_input}\n\nAssistant:"
                response = await self._client.post(
                    f"{OLLAMA_BASE_URL}/generate",
                    headers={
                        "Authorization": f"Bearer {OLLAMA_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "think": False,
                        "options": {"num_predict": 300}
                    }
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract content
            if "message" in data:
                raw_content = data["message"]["content"]
            elif "response" in data:
                raw_content = data["response"]
            else:
                raw_content = str(data)
            
            # Clean to get final answer only
            content = self._extract_final_answer(raw_content)
            
            print(f"[AI] Response: {content[:50]}...")
            
            # Store in history for contextual continuity
            self.history.append(Message(role="user", content=user_input))
            self.history.append(Message(role="assistant", content=content))
            
            return AIResponse(
                content=content,
                provider=AIProvider.OLLAMA,
                model=OLLAMA_MODEL,
                success=True
            )
            
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}"
            print(f"[AI] Error: {error_msg}")
            return AIResponse(
                content="Sorry, I couldn't process that.",
                provider=AIProvider.OLLAMA,
                model=OLLAMA_MODEL,
                success=False,
                error=error_msg
            )
        except Exception as e:
            print(f"[AI] Error: {e}")
            return AIResponse(
                content="Sorry, something went wrong.",
                provider=AIProvider.OLLAMA,
                model=OLLAMA_MODEL,
                success=False,
                error=str(e)
            )
    
    def clear_history(self):
        """Clear conversation history"""
        self.history.clear()
    
    async def cleanup(self):
        """Cleanup resources"""
        await self._client.aclose()


if __name__ == "__main__":
    async def test():
        print("Testing AI Engine...")
        engine = AIEngine()
        
        tests = [
            "Hello!",
            "Tell me a joke",
            "What's the capital of France?"
        ]
        
        for q in tests:
            print(f"\nQ: {q}")
            r = await engine.get_response(q)
            print(f"A: {r.content}")
        
        await engine.cleanup()
    
    asyncio.run(test())
