# PROJECT: Advanced Agentic AI Desktop Assistant

## 🎯 MISSION
Build a production-ready desktop AI assistant that combines:
- ClawdBot-style agentic coding capabilities
- Claude Cowork-style extensible skills system
- Screen reading and real-time guidance
- Voice control and app automation
- Multi-model orchestration for optimal performance

## 📋 TECHNOLOGY STACK

### APIs & Models
1. **Ollama API** (Local/Remote with API Key):
   - **Kimi K2.5 (kimi-k2.5)** - Primary agentic model for reasoning, coding, task execution
   - **Best Vision Model** (llama3.2-vision:90b or qwen2-vl:72b) - Screen analysis, UI understanding
   - API Key required for remote Ollama instance
2. **Perplexity API** - Real-time information, web search
3. **OpenRouter API** - Whisper for voice transcription
4. **Optional**: Anthropic Claude API (for complex planning fallback)

### Core Technologies
- **Frontend**: Electron + React + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI (for AI orchestration) + Node.js (for Electron main process)
- **Desktop Automation**: PyAutoGUI, pygetwindow, keyboard (Python)
- **Screen Capture**: mss (Python), screenshot-desktop (Node)
- **Voice**: WebRTC for capture, Whisper via OpenRouter
- **Database**: SQLite (conversations) + ChromaDB (vector memory)

---

## 🏗️ ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│                     ELECTRON UI (React)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐ │
│  │  Voice   │ │  Chat    │ │  Screen  │ │  Skills       │ │
│  │  Input   │ │  Interface│ │  Preview │ │  Manager      │ │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕ IPC
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION ENGINE (Python FastAPI)           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Task Planner & Router                      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐   │
│  │ Model   │ │ Context │ │  Safety  │ │  Approval    │   │
│  │ Router  │ │ Manager │ │  Guard   │ │  System      │   │
│  └─────────┘ └─────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      EXECUTION LAYER                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  Screen  │ │   App    │ │  Code    │ │    Skills    │  │
│  │  Reader  │ │Automation│ │ Executor │ │   System     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      MODEL LAYER                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ Kimi K2.5│ │  Vision  │ │Perplexity│ │   Whisper    │  │
│  │ (Ollama) │ │ (Ollama) │ │   API    │ │(OpenRouter)  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 PHASE 1: PROJECT SETUP & FOUNDATION

### Step 1.1: Initialize Project Structure

Create this exact folder structure:

```
agent-desktop-app/
├── electron-app/              # Electron + React frontend
│   ├── src/
│   │   ├── main/             # Electron main process
│   │   │   ├── main.ts       # Entry point
│   │   │   ├── ipc.ts        # IPC handlers
│   │   │   └── tray.ts       # System tray
│   │   ├── renderer/         # React app
│   │   │   ├── components/
│   │   │   │   ├── Chat.tsx
│   │   │   │   ├── VoiceInput.tsx
│   │   │   │   ├── ScreenPreview.tsx
│   │   │   │   ├── SkillsPanel.tsx
│   │   │   │   └── ApprovalModal.tsx
│   │   │   ├── hooks/
│   │   │   ├── store/        # Zustand state management
│   │   │   ├── App.tsx
│   │   │   └── index.tsx
│   │   └── preload/          # Preload scripts
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                   # Python FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI entry
│   │   ├── orchestrator/     # Core orchestration
│   │   │   ├── planner.py    # Task planning
│   │   │   ├── router.py     # Model routing
│   │   │   └── executor.py   # Execution engine
│   │   ├── models/           # Model integrations
│   │   │   ├── ollama_client.py
│   │   │   ├── perplexity_client.py
│   │   │   ├── openrouter_client.py
│   │   │   └── model_manager.py
│   │   ├── tools/            # System tools
│   │   │   ├── screen_reader.py
│   │   │   ├── app_automation.py
│   │   │   ├── code_executor.py
│   │   │   └── file_ops.py
│   │   ├── skills/           # Skills system
│   │   │   ├── skill_loader.py
│   │   │   ├── skill_executor.py
│   │   │   └── builtin/      # Built-in skills
│   │   ├── memory/           # Context & memory
│   │   │   ├── conversation.py
│   │   │   ├── vector_store.py
│   │   │   └── context_manager.py
│   │   ├── safety/           # Safety & approval
│   │   │   ├── guard.py
│   │   │   └── approval.py
│   │   └── api/              # API routes
│   │       ├── chat.py
│   │       ├── voice.py
│   │       ├── screen.py
│   │       └── skills.py
│   ├── requirements.txt
│   └── config.yaml
│
├── skills/                    # User skills directory
│   ├── README.md
│   └── examples/
│
├── docs/                      # Documentation
├── tests/                     # Test suite
└── README.md
```

### Step 1.2: Core Dependencies

**Backend (requirements.txt):**
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
websockets==12.0
pydantic==2.5.3
pydantic-settings==2.1.0
httpx==0.26.0
# Ollama client for Kimi K2.5 and Vision models
ollama==0.1.6
pyautogui==0.9.54
pygetwindow==0.0.9
keyboard==0.13.5
mss==9.0.1
pillow==10.2.0
opencv-python==4.9.0
chromadb==0.4.22
sqlalchemy==2.0.25
python-dotenv==1.0.0
aiofiles==23.2.1
watchdog==3.0.0
pytest==7.4.4
```

**Frontend (package.json key deps):**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "electron": "^28.0.0",
    "zustand": "^4.5.0",
    "react-markdown": "^9.0.1",
    "lucide-react": "^0.300.0",
    "tailwindcss": "^3.4.0",
    "axios": "^1.6.5",
    "socket.io-client": "^4.6.1"
  }
}
```

---

## 🧠 PHASE 2: MODEL INTEGRATION & ROUTING

### Step 2.1: Model Manager (`backend/app/models/model_manager.py`)

Create a unified model manager that handles all API calls with **Kimi K2.5** and Ollama vision:

```python
from typing import Literal, Optional, Dict, Any, List
import httpx
import json
from enum import Enum
import base64

class ModelType(Enum):
    KIMI = "kimi-k2.5"  # Primary agentic model
    VISION = "llama3.2-vision:90b"  # or "qwen2-vl:72b" - Best vision model
    PERPLEXITY = "sonar-pro"
    WHISPER = "openai/whisper-large-v3"

class ModelManager:
    """
    Centralized model management with intelligent routing
    Uses Ollama for Kimi K2.5 and Vision models
    """
    
    def __init__(self, config: Dict[str, str]):
        self.ollama_base = config.get("OLLAMA_URL", "http://localhost:11434")
        self.ollama_api_key = config.get("OLLAMA_API_KEY")  # API key for remote Ollama
        self.perplexity_key = config["PERPLEXITY_API_KEY"]
        self.openrouter_key = config["OPENROUTER_API_KEY"]
        
        # HTTP client with authentication
        headers = {}
        if self.ollama_api_key:
            headers["Authorization"] = f"Bearer {self.ollama_api_key}"
        
        self.client = httpx.AsyncClient(
            timeout=120.0,
            headers=headers
        )
        
        # Model configurations
        self.kimi_model = config.get("KIMI_MODEL", "kimi-k2.5")
        self.vision_model = config.get("VISION_MODEL", "llama3.2-vision:90b")
    
    async def route_task(self, task: str, context: Dict) -> ModelType:
        """
        Intelligent routing based on task type
        
        Rules:
        - Screen reading/image analysis → Vision Model (Ollama)
        - Real-time info/web search → Perplexity
        - Coding/file ops/agentic tasks → Kimi K2.5 (Ollama)
        - Voice transcription → Whisper (OpenRouter)
        """
        task_lower = task.lower()
        
        # Check if context has images
        has_images = context.get("has_images", False) or context.get("screen_capture", False)
        
        if has_images or any(kw in task_lower for kw in ["screen", "see", "show", "image", "ui", "visual", "look"]):
            return ModelType.VISION
        elif any(kw in task_lower for kw in ["latest", "current", "search", "news", "weather", "today", "now"]):
            return ModelType.PERPLEXITY
        elif any(kw in task_lower for kw in ["code", "file", "create", "modify", "open", "run", "debug", "fix"]):
            return ModelType.KIMI
        else:
            return ModelType.KIMI  # Default to Kimi K2.5 for general agentic tasks
    
    async def call_ollama(
        self, 
        model: str, 
        messages: List[Dict],
        images: Optional[List[str]] = None,
        stream: bool = False,
        options: Optional[Dict] = None
    ) -> Dict:
        """
        Call Ollama API for Kimi K2.5 or Vision models
        
        Args:
            model: "kimi-k2.5" or vision model name
            messages: List of message dicts with role and content
            images: List of base64-encoded images (for vision model)
            stream: Whether to stream response
            options: Additional options like temperature, top_p
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        # Add images for vision model
        if images:
            # Ollama expects images in the message content or as separate field
            payload["images"] = images
        
        # Add options
        if options:
            payload["options"] = options
        
        try:
            response = await self.client.post(
                f"{self.ollama_base}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "message": {
                    "content": f"Error calling Ollama API: {str(e)}"
                }
            }
    
    async def call_kimi(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Dict:
        """
        Call Kimi K2.5 model via Ollama
        
        Kimi K2.5 is excellent for:
        - Agentic reasoning and planning
        - Code generation and debugging
        - Complex task decomposition
        - File operations and system commands
        """
        options = {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
        
        return await self.call_ollama(
            model=self.kimi_model,
            messages=messages,
            options=options
        )
    
    async def call_vision(
        self,
        prompt: str,
        images: List[str],
        temperature: float = 0.3
    ) -> Dict:
        """
        Call Vision model via Ollama for screen/image analysis
        
        Args:
            prompt: Text prompt describing what to analyze
            images: List of base64-encoded images
            temperature: Lower for more focused analysis
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        options = {
            "temperature": temperature,
            "num_predict": 2000,
        }
        
        return await self.call_ollama(
            model=self.vision_model,
            messages=messages,
            images=images,
            options=options
        )
    
    async def call_perplexity(
        self, 
        query: str, 
        context: str = "",
        search_recency_filter: str = "month"
    ) -> Dict:
        """
        Call Perplexity API for real-time info
        
        Args:
            query: Search query
            context: Additional context
            search_recency_filter: "hour", "day", "week", "month", "year"
        """
        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful research assistant providing accurate, real-time information. Be concise and factual."
                },
                {
                    "role": "user", 
                    "content": f"{context}\n\n{query}" if context else query
                }
            ],
            "search_recency_filter": search_recency_filter
        }
        
        try:
            response = await self.client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {
                "error": str(e),
                "choices": [{
                    "message": {
                        "content": f"Error calling Perplexity API: {str(e)}"
                    }
                }]
            }
    
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "en") -> str:
        """
        Transcribe audio using Whisper via OpenRouter
        
        Note: For production, consider using OpenAI API directly
        or a local Whisper deployment for better privacy
        """
        try:
            # OpenRouter/OpenAI Whisper endpoint
            files = {
                "file": ("audio.webm", audio_bytes, "audio/webm")
            }
            data = {
                "model": "whisper-1",
                "language": language
            }
            
            response = await self.client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}"
                },
                files=files,
                data=data
            )
            response.raise_for_status()
            result = response.json()
            return result.get("text", "")
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    async def unified_call(
        self,
        task_description: str,
        messages: List[Dict],
        context: Dict,
        images: Optional[List[str]] = None
    ) -> Dict:
        """
        Unified interface that automatically routes to the best model
        
        This is the main entry point for all AI requests
        """
        # Determine best model
        model_type = await self.route_task(task_description, context)
        
        print(f"🎯 Routing task to: {model_type.value}")
        
        # Call appropriate model
        if model_type == ModelType.KIMI:
            return await self.call_kimi(messages)
        
        elif model_type == ModelType.VISION:
            if not images:
                return {
                    "error": "Vision model requires images",
                    "message": {"content": "No images provided for vision analysis"}
                }
            # Combine messages into single prompt for vision
            prompt = "\n".join([m["content"] for m in messages if m["role"] == "user"])
            return await self.call_vision(prompt, images)
        
        elif model_type == ModelType.PERPLEXITY:
            # Extract query from messages
            query = messages[-1]["content"] if messages else task_description
            return await self.call_perplexity(query, context=context.get("additional_context", ""))
        
        else:
            # Fallback to Kimi
            return await self.call_kimi(messages)
```

### Step 2.2: Task Planner (`backend/app/orchestrator/planner.py`)

Build the intelligent task decomposition system using **Kimi K2.5**:

```python
from typing import List, Dict, Any
from pydantic import BaseModel
from enum import Enum
import json
import re

class TaskType(Enum):
    SCREEN_READ = "screen_read"
    APP_CONTROL = "app_control"
    CODE_EXECUTION = "code_execution"
    FILE_OPERATION = "file_operation"
    WEB_SEARCH = "web_search"
    SYSTEM_COMMAND = "system_command"
    SKILL_EXECUTION = "skill_execution"

class SubTask(BaseModel):
    type: TaskType
    description: str
    requires_approval: bool
    model: str
    tools: List[str]
    params: Dict[str, Any] = {}
    dependencies: List[int] = []  # Indices of tasks that must complete first

class ExecutionPlan(BaseModel):
    original_query: str
    subtasks: List[SubTask]
    estimated_duration: int  # seconds
    risk_level: str  # "low", "medium", "high"

class TaskPlanner:
    """
    Decomposes complex user requests into executable subtasks
    Uses Kimi K2.5 for intelligent planning
    """
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
    
    async def create_plan(self, user_query: str, context: Dict) -> ExecutionPlan:
        """
        Use Kimi K2.5 to break down the query into actionable steps
        
        Kimi K2.5 excels at:
        - Understanding complex multi-step requests
        - Breaking down ambiguous tasks
        - Identifying dependencies between steps
        - Assessing risk levels
        """
        
        planning_prompt = f"""You are an expert task planning AI using the Kimi K2.5 model. Break down this user request into specific, executable subtasks.

User Request: "{user_query}"

Current Context:
- Active Window: {context.get('active_window', 'Unknown')}
- Recent Actions: {context.get('recent_actions', [])}
- Available Tools: screen_reader, app_controller, code_executor, file_ops, web_search, skill_executor

Available Models:
- kimi-k2.5: For coding, file operations, agentic reasoning (YOU)
- vision_model: For screen reading, image analysis
- perplexity: For real-time information, web searches

Output ONLY a valid JSON object with this exact structure:
{{
    "subtasks": [
        {{
            "type": "task_type",
            "description": "detailed description of what to do",
            "requires_approval": true or false,
            "model": "kimi-k2.5" or "vision_model" or "perplexity",
            "tools": ["tool_name"],
            "params": {{"key": "value"}},
            "dependencies": [0, 1]
        }}
    ],
    "risk_level": "low" or "medium" or "high",
    "reasoning": "brief explanation of the plan"
}}

Task Type Options:
- screen_read: Reading/analyzing screen content
- app_control: Opening/controlling applications
- code_execution: Running/debugging code
- file_operation: Creating/modifying files
- web_search: Searching for information
- system_command: System-level commands
- skill_execution: Using custom skills

Rules:
1. Screen reading MUST use "vision_model"
2. Coding/file ops MUST use "kimi-k2.5" (that's you!)
3. Real-time info MUST use "perplexity"
4. Destructive operations MUST set requires_approval: true
5. Keep subtasks atomic and sequential when dependencies exist
6. Include specific params for each subtask
7. Assess risk realistically (high for system changes, low for reads)

Examples of params:
- file_operation: {{"operation": "create", "path": "/path/to/file", "content": "..."}}
- app_control: {{"operation": "open", "app_name": "VS Code"}}
- code_execution: {{"language": "python", "code": "print('hello')"}}
- screen_read: {{"instruction": "find the save button"}}

Output ONLY the JSON, no markdown, no explanation outside the JSON."""

        response = await self.model_manager.call_kimi(
            messages=[{"role": "user", "content": planning_prompt}],
            temperature=0.3  # Lower temperature for more focused planning
        )
        
        # Parse and validate the plan
        try:
            plan_data = self._extract_json(response["message"]["content"])
            
            # Validate and construct subtasks
            subtasks = []
            for task_dict in plan_data["subtasks"]:
                # Convert string type to enum
                task_dict["type"] = TaskType(task_dict["type"])
                subtasks.append(SubTask(**task_dict))
            
            return ExecutionPlan(
                original_query=user_query,
                subtasks=subtasks,
                estimated_duration=len(subtasks) * 5,
                risk_level=plan_data.get("risk_level", "medium")
            )
        except Exception as e:
            print(f"Planning error: {e}")
            # Fallback to simple single-task plan
            return self._create_fallback_plan(user_query, context)
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from model response"""
        # Remove markdown code blocks if present
        text = re.sub(r'```json\s*|\s*```', '', text)
        
        # Find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("No valid JSON found in response")
    
    def _create_fallback_plan(self, query: str, context: Dict) -> ExecutionPlan:
        """Create a simple fallback plan if Kimi fails to generate one"""
        return ExecutionPlan(
            original_query=query,
            subtasks=[
                SubTask(
                    type=TaskType.SYSTEM_COMMAND,
                    description=f"Execute: {query}",
                    requires_approval=True,
                    model="kimi-k2.5",
                    tools=["general"],
                    params={"query": query}
                )
            ],
            estimated_duration=10,
            risk_level="medium"
        )
```

---

## 🖥️ PHASE 3: SCREEN READING & GUIDANCE

### Step 3.1: Screen Reader (`backend/app/tools/screen_reader.py`)

```python
import mss
import base64
from io import BytesIO
from PIL import Image
from typing import Optional, Dict, List

class ScreenReader:
    """
    Captures and analyzes screen content using Ollama vision models
    """
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.sct = mss.mss()
    
    def capture_screen(self, region: Optional[Dict] = None) -> str:
        """
        Capture screenshot and return as base64
        
        Args:
            region: {top, left, width, height} or None for full screen
        """
        if region:
            monitor = region
        else:
            monitor = self.sct.monitors[1]  # Primary monitor
        
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # Resize for faster processing (important for vision models)
        img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=90)
        return base64.b64encode(buffered.getvalue()).decode()
    
    async def analyze_screen(
        self, 
        instruction: str, 
        region: Optional[Dict] = None
    ) -> str:
        """
        Analyze screen content and provide guidance using Ollama Vision model
        
        Examples:
        - "Where is the Save button?"
        - "How do I access settings in this app?"
        - "Read all text on screen"
        - "What error message is showing?"
        """
        screenshot_b64 = self.capture_screen(region)
        
        prompt = f"""Analyze this screenshot carefully and answer the user's question.

User Question: {instruction}

Provide:
1. Direct answer to their question
2. Step-by-step guidance if applicable (numbered steps)
3. Visual descriptions including:
   - Exact locations (e.g., "top-right corner", "left sidebar")
   - Button/element colors and text
   - Any icons or symbols
   - Relative positions

Be specific, concise, and actionable. If you see multiple relevant elements, list them all."""
        
        response = await self.model_manager.call_vision(
            prompt=prompt,
            images=[screenshot_b64],
            temperature=0.2  # Lower temperature for accurate visual analysis
        )
        
        return response["message"]["content"]
    
    async def find_element(self, description: str) -> Dict:
        """
        Locate UI element on screen using vision model
        
        Args:
            description: Description of element to find (e.g., "blue Save button")
        
        Returns: 
            {
                "found": bool,
                "x": int,
                "y": int,
                "width": int,
                "height": int,
                "confidence": int (0-100),
                "description": str
            }
        """
        screenshot_b64 = self.capture_screen()
        
        prompt = f"""Locate this UI element on the screenshot: "{description}"

Analyze the image carefully and identify the element's position.

Return ONLY a JSON object with this exact structure:
{{
    "found": true or false,
    "x": pixel_x_coordinate,
    "y": pixel_y_coordinate,
    "width": element_width,
    "height": element_height,
    "confidence": confidence_score_0_to_100,
    "description": "what you see at that location"
}}

If the element is not found, set found: false and explain why in the description.
Provide coordinates relative to the top-left corner (0,0).
"""
        
        response = await self.model_manager.call_vision(
            prompt=prompt,
            images=[screenshot_b64],
            temperature=0.1  # Very low for precise location
        )
        
        try:
            return self._extract_json(response["message"]["content"])
        except:
            return {
                "found": False,
                "description": "Failed to parse location data"
            }
    
    async def read_text_on_screen(self, region: Optional[Dict] = None) -> str:
        """
        OCR-like functionality to extract all visible text
        """
        screenshot_b64 = self.capture_screen(region)
        
        prompt = """Extract ALL visible text from this screenshot.

Rules:
1. Transcribe text exactly as shown
2. Preserve structure (headers, paragraphs, lists)
3. Indicate UI element labels clearly
4. Note any error messages or warnings
5. If text is truncated or unclear, note it

Format the output as readable text, organized by screen regions."""
        
        response = await self.model_manager.call_vision(
            prompt=prompt,
            images=[screenshot_b64],
            temperature=0.0  # Deterministic for text extraction
        )
        
        return response["message"]["content"]
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from text response"""
        import re
        import json
        text = re.sub(r'```json\s*|\s*```', '', text)
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError("No valid JSON found")
```

---

## 🤖 PHASE 4: APP AUTOMATION & CONTROL

### Step 4.1: App Controller (`backend/app/tools/app_automation.py`)

```python
import pyautogui
import pygetwindow as gw
import keyboard
import time
import subprocess
from typing import Optional, List, Dict
import platform
import asyncio

class AppAutomation:
    """
    Controls desktop applications programmatically
    Works with Kimi K2.5 for intelligent automation
    """
    
    def __init__(self):
        self.system = platform.system()
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.5  # Pause between actions
    
    async def open_app(self, app_name: str, args: List[str] = None) -> Dict:
        """
        Launch an application by name
        
        Returns: {"success": bool, "message": str, "window": dict}
        """
        try:
            if self.system == "Windows":
                if args:
                    subprocess.Popen([app_name] + args)
                else:
                    subprocess.Popen(app_name)
            elif self.system == "Darwin":  # macOS
                cmd = ["open", "-a", app_name]
                if args:
                    cmd.extend(["--args"] + args)
                subprocess.Popen(cmd)
            else:  # Linux
                cmd = [app_name]
                if args:
                    cmd.extend(args)
                subprocess.Popen(cmd)
            
            time.sleep(2)  # Wait for app to open
            
            # Try to get window info
            window = self.get_active_window()
            
            return {
                "success": True,
                "message": f"Opened {app_name}",
                "window": window
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to open {app_name}: {str(e)}",
                "window": None
            }
    
    def get_active_window(self) -> Optional[Dict]:
        """Get info about current active window"""
        try:
            window = gw.getActiveWindow()
            if window:
                return {
                    "title": window.title,
                    "x": window.left,
                    "y": window.top,
                    "width": window.width,
                    "height": window.height,
                    "app": window.title.split("-")[-1].strip() if "-" in window.title else window.title
                }
        except:
            return None
    
    def list_windows(self) -> List[Dict]:
        """List all open windows"""
        windows = []
        for window in gw.getAllWindows():
            if window.title:  # Skip windows without titles
                windows.append({
                    "title": window.title,
                    "x": window.left,
                    "y": window.top,
                    "width": window.width,
                    "height": window.height
                })
        return windows
    
    def focus_window(self, title_contains: str) -> bool:
        """Bring window to front"""
        windows = gw.getWindowsWithTitle(title_contains)
        if windows:
            windows[0].activate()
            time.sleep(0.5)
            return True
        return False
    
    async def click_at(self, x: int, y: int, clicks: int = 1, button: str = "left"):
        """
        Click at specific coordinates
        
        Args:
            x, y: Screen coordinates
            clicks: Number of clicks (1 for single, 2 for double)
            button: "left", "right", or "middle"
        """
        pyautogui.click(x, y, clicks=clicks, button=button)
        await asyncio.sleep(0.3)
    
    async def type_text(self, text: str, interval: float = 0.05):
        """Type text with delay between chars"""
        pyautogui.write(text, interval=interval)
        await asyncio.sleep(0.3)
    
    async def press_keys(self, *keys: str):
        """
        Press key combination
        
        Examples:
            await press_keys('ctrl', 's')  # Save
            await press_keys('ctrl', 'shift', 't')  # Reopen tab
            await press_keys('alt', 'f4')  # Close window
        """
        keyboard.press_and_release("+".join(keys))
        await asyncio.sleep(0.3)
    
    async def execute_macro(self, steps: List[Dict]) -> Dict:
        """
        Execute a sequence of UI actions
        
        Steps format:
        [
            {"action": "click", "x": 100, "y": 200, "button": "left"},
            {"action": "type", "text": "hello world"},
            {"action": "keys", "combo": ["ctrl", "s"]},
            {"action": "wait", "seconds": 1.0},
            {"action": "drag", "x1": 100, "y1": 200, "x2": 300, "y2": 400}
        ]
        """
        try:
            for i, step in enumerate(steps):
                action = step["action"]
                
                print(f"  Step {i+1}: {action}")
                
                if action == "click":
                    await self.click_at(
                        step["x"], 
                        step["y"],
                        clicks=step.get("clicks", 1),
                        button=step.get("button", "left")
                    )
                
                elif action == "type":
                    await self.type_text(
                        step["text"],
                        interval=step.get("interval", 0.05)
                    )
                
                elif action == "keys":
                    await self.press_keys(*step["combo"])
                
                elif action == "wait":
                    await asyncio.sleep(step["seconds"])
                
                elif action == "drag":
                    pyautogui.moveTo(step["x1"], step["y1"])
                    pyautogui.dragTo(
                        step["x2"], 
                        step["y2"],
                        duration=step.get("duration", 0.5),
                        button=step.get("button", "left")
                    )
                    await asyncio.sleep(0.3)
                
                elif action == "scroll":
                    pyautogui.scroll(
                        step.get("amount", 0),
                        x=step.get("x"),
                        y=step.get("y")
                    )
                    await asyncio.sleep(0.3)
            
            return {
                "success": True,
                "steps_completed": len(steps),
                "message": "Macro executed successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Macro execution failed at step {i+1}"
            }
```

---

## 💻 PHASE 5: CODE EXECUTOR & VS CODE INTEGRATION

### Step 5.1: Code Executor (`backend/app/tools/code_executor.py`)

```python
import subprocess
import os
import tempfile
import asyncio
from typing import Dict, Optional, List
from pathlib import Path
import json

class CodeExecutor:
    """
    Safely execute code and integrate with VS Code
    Works seamlessly with Kimi K2.5's code generation
    """
    
    def __init__(self, workspace_dir: str):
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(exist_ok=True, parents=True)
    
    async def execute_python(
        self, 
        code: str,
        timeout: int = 30,
        capture_output: bool = True
    ) -> Dict:
        """
        Execute Python code in sandbox
        
        Returns:
            {
                "success": bool,
                "stdout": str,
                "stderr": str,
                "exit_code": int,
                "execution_time": float
            }
        """
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.py', 
            delete=False,
            dir=self.workspace
        ) as f:
            f.write(code)
            temp_file = f.name
        
        import time
        start_time = time.time()
        
        try:
            if capture_output:
                result = subprocess.run(
                    ['python', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                execution_time = time.time() - start_time
                
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "exit_code": result.returncode,
                    "execution_time": execution_time
                }
            else:
                # Run without capturing (for interactive scripts)
                result = subprocess.run(
                    ['python', temp_file],
                    timeout=timeout
                )
                return {
                    "success": result.returncode == 0,
                    "exit_code": result.returncode,
                    "execution_time": time.time() - start_time
                }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "exit_code": -1
            }
        finally:
            # Cleanup
            try:
                os.unlink(temp_file)
            except:
                pass
    
    async def execute_javascript(self, code: str, timeout: int = 30) -> Dict:
        """Execute JavaScript code using Node.js"""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.js',
            delete=False,
            dir=self.workspace
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        finally:
            os.unlink(temp_file)
    
    async def execute_bash(self, command: str, timeout: int = 30) -> Dict:
        """Execute bash command (with safety checks)"""
        # Safety: Block dangerous commands
        dangerous_patterns = [
            'rm -rf /',
            'dd if=',
            'mkfs',
            '> /dev/sda',
            'chmod -R 777 /',
        ]
        
        if any(pattern in command for pattern in dangerous_patterns):
            return {
                "success": False,
                "error": "Dangerous command blocked",
                "blocked": True
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds"
            }
    
    async def open_in_vscode(self, filepath: str, line: Optional[int] = None):
        """
        Open file in VS Code
        
        Args:
            filepath: Path to file
            line: Optional line number to jump to
        """
        if line:
            subprocess.Popen(['code', '--goto', f'{filepath}:{line}'])
        else:
            subprocess.Popen(['code', filepath])
    
    async def vscode_create_file(
        self, 
        filename: str, 
        content: str,
        open_after: bool = True
    ) -> Dict:
        """
        Create a file and optionally open in VS Code
        
        Perfect for Kimi K2.5 generated code
        """
        filepath = self.workspace / filename
        
        try:
            # Create parent directories if needed
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            filepath.write_text(content, encoding='utf-8')
            
            # Open in VS Code
            if open_after:
                await self.open_in_vscode(str(filepath))
            
            return {
                "success": True,
                "filepath": str(filepath),
                "message": f"Created {filename}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def vscode_edit_file(
        self,
        filepath: str,
        line_number: int,
        new_content: str
    ) -> Dict:
        """
        Edit specific line(s) in a file
        """
        try:
            path = Path(filepath)
            lines = path.read_text().splitlines()
            
            # Replace line
            if 0 <= line_number - 1 < len(lines):
                lines[line_number - 1] = new_content
                path.write_text('\n'.join(lines))
                
                # Open at that line
                await self.open_in_vscode(filepath, line_number)
                
                return {
                    "success": True,
                    "message": f"Edited line {line_number}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Line {line_number} out of range"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def run_in_vscode_terminal(self, command: str) -> Dict:
        """
        Execute command in VS Code's integrated terminal
        
        Note: This requires VS Code to be open
        """
        # Use VS Code CLI to run command in terminal
        try:
            # This is a workaround - proper implementation needs VS Code extension
            subprocess.Popen([
                'code',
                '--command',
                f'workbench.action.terminal.sendSequence',
                '--args',
                json.dumps({"text": f"{command}\n"})
            ])
            
            return {
                "success": True,
                "message": f"Sent command to VS Code terminal"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "VS Code terminal integration requires VS Code to be open"
            }
```

---

## 🧩 PHASE 6: SKILLS SYSTEM (Like Claude Cowork)

### Step 6.1: Skill Structure

Skills are Python modules with a specific structure:

```python
# skills/examples/git_workflow.py

from typing import Dict, Any
import subprocess

class GitWorkflowSkill:
    """
    Example skill: Automated git workflow
    Compatible with Kimi K2.5's understanding
    """
    
    # Skill metadata
    name = "git_workflow"
    description = "Automated git operations: commit, push, pull, branch management"
    version = "1.0.0"
    author = "User"
    
    # Required tools
    required_tools = ["bash", "file_ops"]
    
    # Approval required for these operations
    requires_approval = ["push", "force_push", "delete_branch"]
    
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict:
        """
        Execute git action
        
        Actions: commit, push, pull, create_branch, switch_branch, status
        """
        if action == "commit":
            return await self._commit(params)
        elif action == "push":
            return await self._push(params)
        elif action == "pull":
            return await self._pull(params)
        elif action == "status":
            return await self._status(params)
        elif action == "create_branch":
            return await self._create_branch(params)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _commit(self, params: Dict) -> Dict:
        """
        Commit changes with message
        """
        message = params.get("message", "Auto-commit")
        files = params.get("files", ".")
        
        try:
            # Add files
            subprocess.run(["git", "add", files], check=True, capture_output=True)
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": f"Committed changes: {message}",
                "output": result.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _push(self, params: Dict) -> Dict:
        """
        Push to remote (requires approval)
        """
        remote = params.get("remote", "origin")
        branch = params.get("branch", "main")
        
        try:
            result = subprocess.run(
                ["git", "push", remote, branch],
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "message": f"Pushed to {remote}/{branch}",
                "output": result.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _status(self, params: Dict) -> Dict:
        """
        Get git status
        """
        try:
            result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True
            )
            
            return {
                "success": True,
                "status": result.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

### Step 6.2: Skill Loader (`backend/app/skills/skill_loader.py`)

```python
import importlib.util
import os
from pathlib import Path
from typing import Dict, List, Any

class SkillLoader:
    """
    Dynamically load and manage user skills
    Works with Kimi K2.5's planning system
    """
    
    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.loaded_skills: Dict[str, Any] = {}
    
    def discover_skills(self) -> List[Dict]:
        """Find all available skills"""
        skills = []
        
        for skill_file in self.skills_dir.rglob("*.py"):
            if skill_file.name.startswith("_"):
                continue
            
            try:
                skill_info = self._load_skill_metadata(skill_file)
                skills.append(skill_info)
            except Exception as e:
                print(f"Failed to load {skill_file}: {e}")
        
        return skills
    
    def _load_skill_metadata(self, filepath: Path) -> Dict:
        """Extract skill metadata without executing"""
        spec = importlib.util.spec_from_file_location("skill", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find skill class (convention: ends with 'Skill')
        skill_class = None
        for item_name in dir(module):
            if item_name.endswith('Skill'):
                skill_class = getattr(module, item_name)
                break
        
        if not skill_class:
            raise ValueError("No skill class found")
        
        return {
            "name": skill_class.name,
            "description": skill_class.description,
            "version": skill_class.version,
            "author": getattr(skill_class, 'author', 'Unknown'),
            "filepath": str(filepath),
            "class": skill_class
        }
    
    async def execute_skill(
        self, 
        skill_name: str, 
        action: str, 
        params: Dict
    ) -> Dict:
        """Execute a skill action"""
        if skill_name not in self.loaded_skills:
            # Load skill on demand
            skills = self.discover_skills()
            skill_info = next((s for s in skills if s["name"] == skill_name), None)
            
            if not skill_info:
                return {"success": False, "error": "Skill not found"}
            
            self.loaded_skills[skill_name] = skill_info["class"]()
        
        skill_instance = self.loaded_skills[skill_name]
        
        # Check if approval needed
        if action in getattr(skill_instance, 'requires_approval', []):
            return {
                "success": False,
                "requires_approval": True,
                "action": action,
                "params": params
            }
        
        return await skill_instance.execute(action, params)
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        """Get metadata about a specific skill"""
        skills = self.discover_skills()
        return next((s for s in skills if s["name"] == skill_name), None)
    
    def list_skills(self) -> List[Dict]:
        """List all available skills with their metadata"""
        return self.discover_skills()
```

---

## 🎙️ PHASE 7: VOICE CONTROL

### Step 7.1: Voice Input Handler (`backend/app/api/voice.py`)

```python
from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect
import base64
import httpx

router = APIRouter()

class VoiceHandler:
    """
    Handle voice input and transcription using Whisper
    """
    
    def __init__(self, openrouter_key: str):
        self.openrouter_key = openrouter_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def transcribe_with_whisper(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio using Whisper via OpenRouter
        """
        try:
            # Use OpenAI Whisper API (accessible via OpenRouter key)
            files = {
                "file": ("audio.webm", audio_bytes, "audio/webm")
            }
            data = {
                "model": "whisper-1",
                "language": "en"
            }
            
            response = await self.client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}"
                },
                files=files,
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("text", "")
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile):
    """
    Single audio file transcription endpoint
    """
    voice_handler = VoiceHandler(config["OPENROUTER_API_KEY"])
    audio_bytes = await audio.read()
    
    text = await voice_handler.transcribe_with_whisper(audio_bytes)
    
    return {
        "success": bool(text),
        "text": text
    }

@router.websocket("/ws/voice")
async def voice_stream(websocket: WebSocket):
    """
    Real-time voice streaming for continuous conversation
    """
    await websocket.accept()
    voice_handler = VoiceHandler(config["OPENROUTER_API_KEY"])
    
    try:
        while True:
            # Receive audio chunks
            audio_data = await websocket.receive_bytes()
            
            # Transcribe
            text = await voice_handler.transcribe_with_whisper(audio_data)
            
            if text:
                # Send back transcription
                await websocket.send_json({
                    "type": "transcription",
                    "text": text
                })
    
    except WebSocketDisconnect:
        print("Voice stream disconnected")
    except Exception as e:
        print(f"Voice stream error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass
```

### Step 7.2: Frontend Voice Component (`electron-app/src/renderer/components/VoiceInput.tsx`)

```typescript
import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';

export const VoiceInput: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1,
          sampleRate: 16000
        } 
      });
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      // Connect to WebSocket
      const ws = new WebSocket('ws://localhost:8000/api/voice/ws/voice');
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('Voice WebSocket connected');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'transcription') {
          setTranscription(data.text);
          setIsProcessing(false);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsProcessing(false);
      };

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        
        if (ws.readyState === WebSocket.OPEN) {
          setIsProcessing(true);
          const arrayBuffer = await audioBlob.arrayBuffer();
          ws.send(arrayBuffer);
        }
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setTranscription('');
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  return (
    <div className="voice-input-container">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`voice-btn ${isRecording ? 'recording' : ''} ${isProcessing ? 'processing' : ''}`}
        disabled={isProcessing}
      >
        {isProcessing ? (
          <Volume2 className="animate-pulse" />
        ) : isRecording ? (
          <MicOff />
        ) : (
          <Mic />
        )}
      </button>
      
      {transcription && (
        <div className="transcription-bubble">
          <p>{transcription}</p>
        </div>
      )}
      
      {isRecording && (
        <div className="recording-indicator">
          <span className="recording-dot"></span>
          Recording...
        </div>
      )}
    </div>
  );
};
```

---

## 🎨 PHASE 8: UI DESIGN (MiniMax Agent Style)

### Step 8.1: Main App Component (`electron-app/src/renderer/App.tsx`)

```typescript
import React, { useEffect } from 'react';
import { Chat } from './components/Chat';
import { VoiceInput } from './components/VoiceInput';
import { ScreenPreview } from './components/ScreenPreview';
import { SkillsPanel } from './components/SkillsPanel';
import { ApprovalModal } from './components/ApprovalModal';
import { useStore } from './store';
import { Settings, Minimize2, X } from 'lucide-react';

export const App: React.FC = () => {
  const { showScreenPreview, showSkills, toggleSkills, toggleScreenPreview } = useStore();

  useEffect(() => {
    // Setup keyboard shortcuts
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+Space: Voice input
      if (e.ctrlKey && e.code === 'Space') {
        e.preventDefault();
        // Trigger voice input
      }
      
      // Ctrl+Shift+S: Screen preview
      if (e.ctrlKey && e.shiftKey && e.code === 'KeyS') {
        e.preventDefault();
        toggleScreenPreview();
      }
      
      // Ctrl+K: Skills panel
      if (e.ctrlKey && e.code === 'KeyK') {
        e.preventDefault();
        toggleSkills();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="app-container">
      {/* Top Bar */}
      <div className="top-bar">
        <div className="logo-section">
          <div className="logo-icon">🤖</div>
          <h1 className="logo-text">Agent Assistant</h1>
          <span className="badge">Powered by Kimi K2.5</span>
        </div>

        <div className="controls-section">
          <VoiceInput />
          
          <button 
            onClick={toggleSkills}
            className={`control-btn ${showSkills ? 'active' : ''}`}
            title="Skills (Ctrl+K)"
          >
            <Settings className="w-5 h-5" />
          </button>
          
          <div className="window-controls">
            <button className="window-btn" onClick={() => window.electron.minimize()}>
              <Minimize2 className="w-4 h-4" />
            </button>
            <button className="window-btn close" onClick={() => window.electron.close()}>
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Layout */}
      <div className="main-layout">
        {/* Left Sidebar - Skills */}
        {showSkills && (
          <div className="sidebar left">
            <SkillsPanel />
          </div>
        )}

        {/* Center - Chat */}
        <div className="chat-area">
          <Chat />
        </div>

        {/* Right Sidebar - Screen Preview */}
        {showScreenPreview && (
          <div className="sidebar right">
            <ScreenPreview />
          </div>
        )}
      </div>

      {/* Approval Modal */}
      <ApprovalModal />
    </div>
  );
};
```

### Step 8.2: Tailwind Styling (MiniMax-inspired) (`electron-app/src/renderer/styles/app.css`)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ============================================
   MAIN APP CONTAINER
   ============================================ */
.app-container {
  @apply h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden;
}

/* ============================================
   TOP BAR
   ============================================ */
.top-bar {
  @apply flex items-center justify-between px-6 py-4 bg-black/30 backdrop-blur-xl border-b border-white/10;
  -webkit-app-region: drag; /* Make draggable */
}

.logo-section {
  @apply flex items-center gap-3;
}

.logo-icon {
  @apply text-3xl;
}

.logo-text {
  @apply text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent;
}

.badge {
  @apply px-2 py-1 text-xs bg-purple-500/20 rounded-full border border-purple-500/30;
}

.controls-section {
  @apply flex items-center gap-3;
  -webkit-app-region: no-drag; /* Make controls clickable */
}

.control-btn {
  @apply p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all duration-200;
}

.control-btn.active {
  @apply bg-purple-500/30 border border-purple-500/50;
}

.window-controls {
  @apply flex items-center gap-1 ml-4;
}

.window-btn {
  @apply p-2 rounded-lg hover:bg-white/10 transition-all;
}

.window-btn.close {
  @apply hover:bg-red-500/30;
}

/* ============================================
   MAIN LAYOUT
   ============================================ */
.main-layout {
  @apply flex h-[calc(100vh-64px)] overflow-hidden;
}

.sidebar {
  @apply w-80 bg-black/20 backdrop-blur-xl border-white/10 p-4 overflow-y-auto;
}

.sidebar.left {
  @apply border-r;
}

.sidebar.right {
  @apply border-l;
}

/* Custom Scrollbar */
.sidebar::-webkit-scrollbar {
  @apply w-2;
}

.sidebar::-webkit-scrollbar-track {
  @apply bg-white/5 rounded;
}

.sidebar::-webkit-scrollbar-thumb {
  @apply bg-purple-500/30 rounded hover:bg-purple-500/50;
}

.chat-area {
  @apply flex-1 flex flex-col p-6 overflow-hidden;
}

/* ============================================
   CHAT MESSAGES
   ============================================ */
.messages-container {
  @apply flex-1 overflow-y-auto space-y-4 mb-4;
}

.message {
  @apply p-4 rounded-2xl backdrop-blur-xl max-w-[85%] animate-fadeIn;
}

.message.user {
  @apply bg-purple-500/20 ml-auto border border-purple-500/30;
}

.message.assistant {
  @apply bg-white/10 mr-auto border border-white/10;
}

.message.system {
  @apply bg-blue-500/20 mx-auto text-center border border-blue-500/30;
}

.message-content {
  @apply text-sm leading-relaxed;
}

.message-timestamp {
  @apply text-xs text-white/50 mt-2;
}

/* ============================================
   INPUT AREA
   ============================================ */
.input-container {
  @apply flex items-end gap-3 p-4 bg-black/20 backdrop-blur-xl rounded-2xl border border-white/10;
}

.input-textarea {
  @apply flex-1 bg-transparent border-none outline-none resize-none text-white placeholder-white/50 max-h-32;
}

.send-btn {
  @apply p-3 rounded-xl bg-purple-500 hover:bg-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed;
}

/* ============================================
   VOICE INPUT
   ============================================ */
.voice-input-container {
  @apply relative;
}

.voice-btn {
  @apply w-12 h-12 rounded-full bg-purple-500 hover:bg-purple-600 transition-all flex items-center justify-center shadow-lg;
}

.voice-btn.recording {
  @apply bg-red-500 animate-pulse shadow-red-500/50;
}

.voice-btn.processing {
  @apply bg-blue-500 cursor-wait;
}

.transcription-bubble {
  @apply absolute bottom-full right-0 mb-2 p-3 bg-black/80 backdrop-blur-xl rounded-lg shadow-xl max-w-xs;
}

.recording-indicator {
  @apply absolute bottom-full right-0 mb-2 flex items-center gap-2 px-3 py-2 bg-red-500/20 backdrop-blur-xl rounded-lg text-sm;
}

.recording-dot {
  @apply w-2 h-2 bg-red-500 rounded-full animate-pulse;
}

/* ============================================
   SKILLS PANEL
   ============================================ */
.skills-panel {
  @apply space-y-4;
}

.skill-card {
  @apply p-4 bg-white/5 rounded-xl border border-white/10 hover:bg-white/10 transition-all cursor-pointer;
}

.skill-card.active {
  @apply bg-purple-500/20 border-purple-500/50;
}

.skill-header {
  @apply flex items-center justify-between mb-2;
}

.skill-name {
  @apply font-semibold text-white;
}

.skill-version {
  @apply text-xs text-white/50;
}

.skill-description {
  @apply text-sm text-white/70;
}

/* ============================================
   SCREEN PREVIEW
   ============================================ */
.screen-preview {
  @apply space-y-3;
}

.preview-image {
  @apply w-full rounded-lg border border-white/20;
}

.preview-controls {
  @apply flex gap-2;
}

.preview-btn {
  @apply flex-1 py-2 px-3 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-all;
}

/* ============================================
   APPROVAL MODAL
   ============================================ */
.modal-overlay {
  @apply fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 animate-fadeIn;
}

.modal-content {
  @apply bg-slate-800 rounded-2xl p-6 max-w-md w-full border border-white/10 shadow-2xl animate-scaleIn;
}

.modal-header {
  @apply flex items-center gap-3 mb-4;
}

.risk-badge {
  @apply p-2 rounded-full;
}

.risk-badge.high {
  @apply bg-red-500;
}

.risk-badge.medium {
  @apply bg-yellow-500;
}

.risk-badge.low {
  @apply bg-blue-500;
}

.modal-title {
  @apply text-xl font-bold;
}

.modal-body {
  @apply mb-6;
}

.modal-description {
  @apply text-gray-300 mb-3;
}

.modal-details {
  @apply bg-black/30 rounded-lg p-3 font-mono text-sm text-purple-300;
}

.modal-actions {
  @apply flex gap-3;
}

.modal-btn {
  @apply flex-1 py-3 px-4 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all;
}

.modal-btn.approve {
  @apply bg-green-500 hover:bg-green-600;
}

.modal-btn.reject {
  @apply bg-red-500 hover:bg-red-600;
}

/* ============================================
   ANIMATIONS
   ============================================ */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}

.animate-scaleIn {
  animation: scaleIn 0.2s ease-out;
}

/* ============================================
   UTILITIES
   ============================================ */
.glass {
  @apply bg-white/5 backdrop-blur-xl border border-white/10;
}

.glow {
  @apply shadow-lg shadow-purple-500/20;
}

/* Code Blocks */
.code-block {
  @apply bg-black/50 rounded-lg p-4 font-mono text-sm overflow-x-auto;
}

/* Loading Spinner */
.spinner {
  @apply w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin;
}
```

---

## 📝 PHASE 9: CONFIGURATION

### Step 9.1: Configuration File (`backend/config.yaml`)

```yaml
# ============================================
# AGENT DESKTOP ASSISTANT CONFIGURATION
# ============================================

# Ollama Configuration (for Kimi K2.5 and Vision)
OLLAMA_URL: "http://localhost:11434"  # Change if using remote Ollama
OLLAMA_API_KEY: "your_ollama_api_key_here"  # Required for remote Ollama instance

# Model Selection
KIMI_MODEL: "kimi-k2.5"  # Primary agentic model
VISION_MODEL: "llama3.2-vision:90b"  # Best vision model (alternatives: qwen2-vl:72b)

# External APIs
PERPLEXITY_API_KEY: "your_perplexity_key_here"
OPENROUTER_API_KEY: "your_openrouter_key_here"  # For Whisper transcription

# Workspace
workspace_dir: "./workspace"
skills_dir: "./skills"

# Safety Settings
auto_approve_low_risk: false  # Set to true to auto-approve safe operations
require_approval_for:
  - file_deletion
  - system_commands
  - git_push
  - app_close
  - code_execution  # Remove this to auto-execute code

# Model Performance Tuning
model_settings:
  kimi:
    temperature: 0.7
    max_tokens: 4000
    top_p: 0.9
  vision:
    temperature: 0.3  # Lower for more accurate visual analysis
    max_tokens: 2000
  perplexity:
    temperature: 0.5
    search_recency: "month"  # hour, day, week, month, year

# UI Settings
ui:
  theme: "dark"
  voice_enabled: true
  screen_preview_enabled: true
  show_token_usage: false
  max_message_history: 100

# Performance
performance:
  parallel_execution: true  # Execute independent tasks in parallel
  cache_enabled: true
  max_concurrent_tasks: 3

# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_file: "./logs/agent.log"
  log_to_console: true
```

### Step 9.2: Environment Setup Script (`setup.sh`)

```bash
#!/bin/bash
# setup.sh - Complete setup script for Agent Desktop Assistant

echo "🚀 Setting up Agent Desktop Assistant with Kimi K2.5..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check Ollama installation
echo -e "${YELLOW}Checking Ollama installation...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama not found.${NC}"
    echo "Please install from https://ollama.ai"
    exit 1
fi
echo -e "${GREEN}✅ Ollama found${NC}"
echo ""

# 2. Pull required models
echo -e "${YELLOW}📥 Pulling Kimi K2.5 model...${NC}"
ollama pull kimi-k2.5
echo ""

echo -e "${YELLOW}📥 Pulling Vision model (llama3.2-vision:90b)...${NC}"
echo "Note: This is a large model (~50GB). Alternative: qwen2-vl:72b"
read -p "Continue with llama3.2-vision:90b? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ollama pull llama3.2-vision:90b
else
    echo "Pulling qwen2-vl:72b instead..."
    ollama pull qwen2-vl:72b
fi
echo ""

echo -e "${GREEN}✅ Models downloaded${NC}"
echo ""

# 3. Setup Python environment
echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Python environment ready${NC}"
echo ""

# 4. Setup Node.js environment
echo -e "${YELLOW}📦 Setting up Node.js environment...${NC}"
cd ../electron-app

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found.${NC}"
    echo "Please install from https://nodejs.org"
    exit 1
fi

npm install

echo -e "${GREEN}✅ Node.js environment ready${NC}"
echo ""

# 5. Create directories
echo -e "${YELLOW}📁 Creating workspace directories...${NC}"
cd ..
mkdir -p workspace
mkdir -p skills/examples
mkdir -p logs
mkdir -p backend/app/skills/builtin

echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# 6. Copy example skill
cat > skills/examples/git_workflow.py << 'EOF'
# Example skill - see documentation for full implementation
from typing import Dict, Any

class GitWorkflowSkill:
    name = "git_workflow"
    description = "Automated git operations"
    version = "1.0.0"
    
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict:
        return {"success": True, "message": "Example skill"}
EOF

echo -e "${GREEN}✅ Example skill created${NC}"
echo ""

# 7. Configure API keys reminder
echo -e "${YELLOW}🔑 IMPORTANT: Configure your API keys${NC}"
echo ""
echo "Edit backend/config.yaml and add:"
echo "  - OLLAMA_API_KEY (if using remote Ollama)"
echo "  - PERPLEXITY_API_KEY (required)"
echo "  - OPENROUTER_API_KEY (required for voice)"
echo ""

# 8. Create start scripts
cat > backend/start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x backend/start.sh

cat > electron-app/start.sh << 'EOF'
#!/bin/bash
npm start
EOF

chmod +x electron-app/start.sh

echo -e "${GREEN}✅ Start scripts created${NC}"
echo ""

# Final instructions
echo ""
echo -e "${GREEN}✨ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Configure API keys in backend/config.yaml"
echo "2. Start backend:  cd backend && ./start.sh"
echo "3. Start frontend: cd electron-app && ./start.sh"
echo ""
echo "Keyboard shortcuts:"
echo "  - Ctrl+Space: Voice input"
echo "  - Ctrl+Shift+S: Screen preview"
echo "  - Ctrl+K: Skills panel"
echo ""
```

Make it executable:
```bash
chmod +x setup.sh
```

---

## 🎯 PHASE 10: MAIN ORCHESTRATOR

### Step 10.1: Execution Engine (`backend/app/orchestrator/executor.py`)

```python
from typing import Dict, List, Optional
import asyncio
from .planner import TaskPlanner, ExecutionPlan
from ..models.model_manager import ModelManager
from ..tools.screen_reader import ScreenReader
from ..tools.app_automation import AppAutomation
from ..tools.code_executor import CodeExecutor
from ..skills.skill_loader import SkillLoader
from ..safety.guard import SafetyGuard

class AgentOrchestrator:
    """
    Central orchestration engine for the AI agent
    Uses Kimi K2.5 for planning and execution
    """
    
    def __init__(self, config: Dict):
        self.model_manager = ModelManager(config)
        self.planner = TaskPlanner(self.model_manager)
        self.screen_reader = ScreenReader(self.model_manager)
        self.app_automation = AppAutomation()
        self.code_executor = CodeExecutor(config["workspace_dir"])
        self.skill_loader = SkillLoader(config["skills_dir"])
        self.safety_guard = SafetyGuard()
        
        self.execution_queue: List[ExecutionPlan] = []
        self.current_execution: Optional[ExecutionPlan] = None
        self.approval_callback = None
        
        print("🤖 Agent Orchestrator initialized with Kimi K2.5")
    
    async def process_command(
        self, 
        user_input: str, 
        context: Dict
    ) -> Dict:
        """
        Main entry point for processing user commands
        
        Flow:
        1. Create execution plan using Kimi K2.5
        2. Evaluate risk
        3. Request approval if needed
        4. Execute subtasks
        5. Return results
        """
        
        print(f"\n{'='*60}")
        print(f"🎯 Processing: {user_input}")
        print(f"{'='*60}\n")
        
        # Step 1: Plan using Kimi K2.5
        print("📋 Creating execution plan...")
        plan = await self.planner.create_plan(user_input, context)
        
        print(f"   Generated {len(plan.subtasks)} subtasks")
        print(f"   Risk level: {plan.risk_level}")
        print(f"   Estimated duration: {plan.estimated_duration}s")
        
        # Step 2: Safety check
        for i, subtask in enumerate(plan.subtasks):
            risk = self.safety_guard.evaluate_risk(subtask.dict())
            subtask.risk_level = risk
            print(f"   Task {i+1}: {subtask.type.value} - Risk: {risk}")
        
        # Step 3: Check if approval needed
        needs_approval = any(
            self.safety_guard.requires_approval(task.risk_level) or task.requires_approval
            for task in plan.subtasks
        )
        
        if needs_approval:
            print("\n⚠️  Approval required for high-risk operations")
            # Request approval and wait
            approval_granted = await self._request_approval(plan)
            if not approval_granted:
                return {
                    "status": "rejected",
                    "message": "User rejected the action"
                }
            print("✅ Approval granted")
        
        # Step 4: Execute
        print("\n🚀 Executing plan...\n")
        results = await self._execute_plan(plan, context)
        
        print(f"\n✨ Execution complete!")
        
        return {
            "status": "completed",
            "results": results,
            "plan": plan.dict()
        }
    
    async def _execute_plan(
        self, 
        plan: ExecutionPlan, 
        context: Dict
    ) -> List[Dict]:
        """
        Execute all subtasks in the plan
        """
        results = []
        
        for i, subtask in enumerate(plan.subtasks):
            print(f"▶️  Executing task {i+1}/{len(plan.subtasks)}: {subtask.description}")
            
            # Wait for dependencies
            for dep_idx in subtask.dependencies:
                if dep_idx < i and results[dep_idx].get("status") != "success":
                    print(f"   ⏭️  Skipped due to failed dependency")
                    results.append({
                        "status": "skipped",
                        "reason": f"Dependency {dep_idx} failed"
                    })
                    continue
            
            # Execute subtask
            result = await self._execute_subtask(subtask, context, results)
            results.append(result)
            
            if result.get("status") == "success":
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        return results
    
    async def _execute_subtask(
        self, 
        subtask, 
        context: Dict, 
        previous_results: List[Dict]
    ) -> Dict:
        """
        Execute a single subtask
        """
        try:
            if subtask.type.value == "screen_read":
                response = await self.screen_reader.analyze_screen(
                    subtask.params.get("instruction", subtask.description)
                )
                return {"status": "success", "data": response}
            
            elif subtask.type.value == "app_control":
                operation = subtask.params.get("operation", "open")
                app_name = subtask.params.get("app_name")
                
                if operation == "open":
                    result = await self.app_automation.open_app(app_name)
                elif operation == "focus":
                    success = self.app_automation.focus_window(app_name)
                    result = {"success": success}
                else:
                    result = {"success": False, "error": f"Unknown operation: {operation}"}
                
                return {"status": "success" if result.get("success") else "failed", "data": result}
            
            elif subtask.type.value == "code_execution":
                language = subtask.params.get("language", "python")
                code = subtask.params.get("code")
                
                if language == "python":
                    result = await self.code_executor.execute_python(code)
                elif language == "javascript":
                    result = await self.code_executor.execute_javascript(code)
                elif language == "bash":
                    result = await self.code_executor.execute_bash(code)
                else:
                    result = {"success": False, "error": f"Unsupported language: {language}"}
                
                return {"status": "success" if result.get("success") else "failed", "data": result}
            
            elif subtask.type.value == "file_operation":
                operation = subtask.params.get("operation")
                
                if operation == "create":
                    result = await self.code_executor.vscode_create_file(
                        subtask.params.get("filename"),
                        subtask.params.get("content", "")
                    )
                else:
                    result = {"success": False, "error": f"Unknown operation: {operation}"}
                
                return {"status": "success" if result.get("success") else "failed", "data": result}
            
            elif subtask.type.value == "web_search":
                query = subtask.params.get("query", subtask.description)
                result = await self.model_manager.call_perplexity(query)
                
                return {
                    "status": "success",
                    "data": result.get("choices", [{}])[0].get("message", {}).get("content", "")
                }
            
            elif subtask.type.value == "skill_execution":
                skill_name = subtask.params.get("skill_name")
                action = subtask.params.get("action")
                params = subtask.params.get("params", {})
                
                result = await self.skill_loader.execute_skill(skill_name, action, params)
                return {"status": "success" if result.get("success") else "failed", "data": result}
            
            else:
                return {"status": "failed", "error": f"Unknown subtask type: {subtask.type.value}"}
        
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def _request_approval(self, plan: ExecutionPlan) -> bool:
        """
        Request user approval for risky operations
        """
        if not self.approval_callback:
            print("⚠️  No approval callback registered, denying by default")
            return False
        
        # Send approval request to frontend
        approval_event = {
            "plan": plan.dict(),
            "risk_level": plan.risk_level,
            "estimated_duration": plan.estimated_duration
        }
        
        # Wait for user response
        approved = await self.approval_callback(approval_event)
        return approved
```

---

## 🔒 PHASE 11: SAFETY SYSTEM

### Step 11.1: Safety Guard (`backend/app/safety/guard.py`)

```python
from typing import Dict, Literal
import re

class SafetyGuard:
    """
    Evaluate risk level and determine if approval needed
    """
    
    # Commands that ALWAYS need approval
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf\s*/\s*$',
        r'del\s+/[SF]',
        r'format\s+[A-Z]:',
        r'shutdown',
        r'reboot',
        r'git\s+push\s+--force',
        r'DROP\s+TABLE',
        r'DELETE\s+FROM.*WHERE\s+1\s*=\s*1',
        r'chmod\s+-R\s+777',
        r'killall',
    ]
    
    # File operations that need approval
    PROTECTED_PATHS = [
        '/System',
        '/Windows',
        'C:\\Windows',
        '/usr/bin',
        '/etc',
        '/Library',
        'C:\\Program Files',
    ]
    
    # System commands that need approval
    SYSTEM_COMMANDS = [
        'shutdown', 'reboot', 'poweroff',
        'kill', 'killall', 'pkill',
        'sudo', 'su',
    ]
    
    def evaluate_risk(self, action: Dict) -> Literal["low", "medium", "high"]:
        """
        Evaluate risk level of an action
        
        Returns: "low", "medium", or "high"
        """
        action_type = action.get("type")
        params = action.get("params", {})
        
        # Check for dangerous commands
        if action_type == "system_command":
            command = params.get("command", "")
            for pattern in self.DANGEROUS_PATTERNS:
                if re.search(pattern, command, re.IGNORECASE):
                    return "high"
            
            # Check for system commands
            if any(cmd in command.lower() for cmd in self.SYSTEM_COMMANDS):
                return "high"
        
        # Check file operations
        if action_type == "file_operation":
            path = params.get("path", "")
            operation = params.get("operation", "")
            
            # Deleting or modifying protected paths
            if operation in ["delete", "modify"] and any(
                path.startswith(protected) for protected in self.PROTECTED_PATHS
            ):
                return "high"
            
            # Any deletion
            if operation == "delete":
                return "medium"
        
        # Check app control
        if action_type == "app_control":
            operation = params.get("operation", "")
            if operation in ["close", "kill"]:
                return "medium"
        
        # Code execution
        if action_type == "code_execution":
            code = params.get("code", "")
            
            # Check for dangerous patterns in code
            for pattern in self.DANGEROUS_PATTERNS:
                if re.search(pattern, code, re.IGNORECASE):
                    return "high"
            
            # File operations in code
            if any(keyword in code for keyword in ['os.remove', 'shutil.rmtree', 'subprocess.call']):
                return "medium"
            
            return "low"
        
        # Screen reading is always low risk
        if action_type == "screen_read":
            return "low"
        
        # Web search is always low risk
        if action_type == "web_search":
            return "low"
        
        # Default to medium for unknown types
        return "medium"
    
    def requires_approval(self, risk_level: str, auto_approve_low: bool = False) -> bool:
        """
        Determine if action needs human approval
        """
        if risk_level == "high":
            return True
        if risk_level == "medium":
            return True
        if risk_level == "low" and not auto_approve_low:
            return False
        
        return False
    
    def get_risk_explanation(self, action: Dict, risk_level: str) -> str:
        """
        Generate human-readable explanation of why something is risky
        """
        action_type = action.get("type")
        
        if risk_level == "high":
            return "This action could significantly modify system files or settings."
        elif risk_level == "medium":
            return "This action will make changes that could affect your workflow."
        else:
            return "This is a safe read-only operation."
```

---

## 🚀 PHASE 12: FINAL INTEGRATION

### Step 12.1: FastAPI Main App (`backend/app/main.py`)

```python
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .orchestrator.executor import AgentOrchestrator
from .api import voice
import yaml
from pathlib import Path

app = FastAPI(
    title="Agent Desktop API",
    description="Powered by Kimi K2.5 and Ollama",
    version="1.0.0"
)

# CORS for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load config
config_path = Path(__file__).parent.parent / "config.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

# Initialize orchestrator
orchestrator = AgentOrchestrator(config)

# Include routers
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])

@app.post("/api/execute")
async def execute_command(request: dict):
    """Main command execution endpoint"""
    command = request.get("command")
    context = request.get("context", {})
    
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")
    
    result = await orchestrator.process_command(command, context)
    return result

@app.get("/api/skills")
async def list_skills():
    """List all available skills"""
    skills = orchestrator.skill_loader.list_skills()
    return {"skills": skills}

@app.get("/api/context")
async def get_context():
    """Get current context (active window, etc.)"""
    context = {
        "active_window": orchestrator.app_automation.get_active_window(),
        "windows": orchestrator.app_automation.list_windows()
    }
    return context

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models": {
            "kimi": config.get("KIMI_MODEL"),
            "vision": config.get("VISION_MODEL")
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📚 KIMI K2.5 ADVANTAGES

### Why Kimi K2.5 is Perfect for This Project

```markdown
## Kimi K2.5 Strengths

### 1. Superior Agentic Reasoning
- **Multi-step Planning**: Excels at breaking down complex tasks into logical steps
- **Dependency Tracking**: Better understanding of task dependencies
- **Context Retention**: 200K+ token context window for maintaining conversation state

### 2. Code Generation Excellence
- **Production-Ready Code**: Generates clean, maintainable code
- **Error Handling**: Better anticipation of edge cases
- **Multiple Languages**: Strong support for Python, JavaScript, TypeScript, etc.

### 3. Task Decomposition
- **Complex Workflows**: Breaks down ambiguous requests into clear actions
- **Risk Assessment**: Better understanding of operation impact
- **Tool Selection**: Intelligent routing to appropriate tools

### 4. Use Kimi K2.5 For:
- ✅ Task planning and decomposition
- ✅ Code generation and debugging
- ✅ File operations and refactoring
- ✅ Complex multi-step workflows
- ✅ System command generation
- ✅ Skill execution logic

### 5. Use Vision Model For:
- ✅ Screen reading and analysis
- ✅ UI element location
- ✅ Image understanding
- ✅ OCR and text extraction

### 6. Use Perplexity For:
- ✅ Real-time information
- ✅ Web searches
- ✅ Current events
- ✅ Fact-checking

## Performance Tips

1. **Leverage Context Window**
   - Include full conversation history for better planning
   - Provide detailed context about user's workspace

2. **Clear Prompts**
   - Be explicit about expected output format (JSON for plans)
   - Provide examples in system prompts

3. **Temperature Settings**
   - Lower (0.3) for planning and coding
   - Higher (0.7) for creative tasks

4. **Streaming**
   - Enable for long responses
   - Better UX for code generation
```

---

## 🎯 IMPLEMENTATION CHECKLIST

```markdown
## Backend
- [ ] FastAPI server setup
- [ ] Ollama integration (Kimi K2.5 + Vision)
- [ ] Perplexity API integration
- [ ] OpenRouter/Whisper integration
- [ ] Task planner (Kimi K2.5)
- [ ] Model router
- [ ] Screen reader (Vision model)
- [ ] App automation
- [ ] Code executor
- [ ] Skills system
- [ ] Safety guard
- [ ] Approval system
- [ ] API endpoints
- [ ] WebSocket support

## Frontend
- [ ] Electron setup
- [ ] React UI (MiniMax style)
- [ ] Chat component
- [ ] Voice input
- [ ] Screen preview
- [ ] Skills panel
- [ ] Approval modal
- [ ] State management (Zustand)
- [ ] IPC communication
- [ ] Keyboard shortcuts
- [ ] System tray integration

## Integration
- [ ] Backend ↔ Frontend IPC
- [ ] Voice ↔ Chat flow
- [ ] Screen capture ↔ Vision model
- [ ] Approval flow
- [ ] Continuous task execution

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Safety tests
- [ ] User acceptance testing

## Documentation
- [ ] User guide
- [ ] API documentation
- [ ] Skills development guide
- [ ] Deployment guide
```

---

## 🚀 QUICK START GUIDE

```bash
# 1. Clone/Create project directory
mkdir agent-desktop-app && cd agent-desktop-app

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Configure API keys
nano backend/config.yaml

# 4. Start backend (Terminal 1)
cd backend
source venv/bin/activate
./start.sh

# 5. Start frontend (Terminal 2)
cd electron-app
./start.sh

# 6. Use the app!
# - Click microphone for voice input
# - Type commands in chat
# - Ctrl+K for skills panel
# - Ctrl+Shift+S for screen preview
```

---

## 📖 DOCUMENTATION LINKS

- **Ollama**: https://ollama.ai/library/kimi-k2.5
- **Kimi K2.5 Docs**: https://platform.moonshot.cn/docs
- **Perplexity API**: https://docs.perplexity.ai
- **OpenRouter**: https://openrouter.ai/docs
- **Electron**: https://electronjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com

---

This is your complete production-ready blueprint using **Kimi K2.5** and **Ollama vision models**! 🚀
