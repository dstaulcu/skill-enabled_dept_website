# AI-Enhanced Air-Gapped Department Website

> A modular, embeddable AI chat interface with enterprise tool integrations, designed for air-gapped environments. Built with Next.js, FastAPI, and Ollama for local LLM deployment.

[![Status](https://img.shields.io/badge/status-mvp-green)]() [![License](https://img.shields.io/badge/license-internal-blue)]()

## 📖 Overview

This project provides a complete solution for embedding AI-powered chat assistants into department websites across diverse platforms (WordPress, SharePoint, Confluence, static sites). The architecture supports:

- **Air-gapped deployment** with local LLM inference (Ollama)
- **Dynamic theming** for seamless visual integration
- **Certificate-based authentication** with development simulation
- **Streaming chat responses** with real-time feedback
- **Enterprise tool integration** (Jira, Confluence, SharePoint via MCP)
- **Multi-tenancy** with department-level data isolation
- **Platform-agnostic embedding** via iframe with security controls

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    subgraph "Host Environment"
        WP[WordPress/SharePoint/Static Site<br/>Port 3000]
    end
    
    subgraph "Chat Application"
        FE[Next.js Frontend<br/>Port 3001<br/>Dynamic Theming]
        BE[FastAPI Backend<br/>Port 8000<br/>Auth + Chat]
    end
    
    subgraph "AI & Data Layer"
        OLLAMA[Ollama LLM<br/>llama3:latest<br/>Local Inference]
        DB[(SQLite<br/>Chat History<br/>User Sessions)]
        FAISS[(FAISS<br/>Vector Store<br/>RAG)]
    end
    
    subgraph "Enterprise Tools"
        JIRA[Jira<br/>Mock/Real API]
        CONF[Confluence<br/>Mock/Real API]
        SP[SharePoint<br/>Mock/Real API]
    end
    
    WP -->|iframe embed| FE
    FE -->|HTTP/SSE| BE
    BE -->|OpenAI API| OLLAMA
    BE -->|Persist| DB
    BE -->|RAG Query| FAISS
    BE -->|MCP| JIRA
    BE -->|MCP| CONF
    BE -->|MCP| SP
    
    style WP fill:#e1f5ff
    style FE fill:#b3e5fc
    style BE fill:#81d4fa
    style OLLAMA fill:#4fc3f7
    style DB fill:#29b6f6
    style FAISS fill:#29b6f6
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Host as Host Site<br/>(Port 3000)
    participant FE as Frontend<br/>(Port 3001)
    participant BE as Backend<br/>(Port 8000)
    participant Ollama as Ollama LLM
    
    User->>Host: Visit department page
    Note over Host: Extract user identity<br/>from client cert (prod)<br/>or use mockUser param (dev)
    Host->>FE: Load iframe with<br/>?mockUser=john.doe@dept.gov
    FE->>FE: Apply theme from URL params
    User->>FE: Type message
    FE->>BE: POST /api/chat/stream<br/>X-Mock-User: john.doe@dept.gov
    BE->>BE: Generate JWT from identity
    BE->>Ollama: Streaming chat request<br/>with user context
    Ollama-->>BE: Stream response chunks
    BE-->>FE: SSE stream
    FE-->>User: Display streaming response
```

### Data Flow

```mermaid
flowchart LR
    A[User Input] --> B{Frontend}
    B --> C[Backend API]
    C --> D{Auth Middleware}
    D -->|Dev Mode| E[Mock User Header]
    D -->|Prod Mode| F[JWT Validation]
    E --> G[Generate/Verify JWT]
    F --> G
    G --> H{Chat Endpoint}
    H --> I[Add System Context]
    I --> J[Ollama API Call]
    J --> K[Stream Response]
    K --> L[SSE to Frontend]
    L --> B
    B --> M[Display to User]
    
    H -.->|Future| N[(SQLite<br/>Persist)]
    H -.->|Future| O[(FAISS<br/>RAG)]
    H -.->|Future| P[MCP Connectors]
    
    style D fill:#ffeb3b
    style G fill:#ffc107
    style J fill:#4caf50
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **Ollama** with llama3 model installed
- **Git**

### Initial Setup

1. **Clone and navigate to project:**
   ```bash
   cd /Users/dstaulcu/code/skill-enabled_dept_website
   ```

2. **Install Ollama and llama3 model (if not already installed):**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   The default `.env` is pre-configured for Ollama on localhost.

4. **Install dependencies:**

   **Host Site:**
   ```bash
   cd host-site
   npm install
   cd ..
   ```

   **Frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

   **Backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

### Running the Services

You'll need **three terminal windows**:

**Terminal 1 - Host Site (Port 3000):**
```bash
cd host-site
python3 -m http.server 3000
# Or use: node server.js (requires: npm install express)
```
Visit http://localhost:3000 to see the department landing page with embedded chat.

**Terminal 2 - Frontend (Port 3001):**
```bash
cd frontend
npm run dev
```
The chat interface runs on http://localhost:3001 (embedded in host-site via iframe).

**Terminal 3 - Backend (Port 8000):**
```bash
cd backend
source ../.venv/bin/activate  # Adjust path if needed
PYTHONPATH=$PWD python -m uvicorn app.main:app --reload --port 8000
```
API backend runs on http://localhost:8000.

### Testing the Setup

1. **Verify Ollama is running:**
   ```bash
   ollama list  # Should show llama3:latest
   ```

2. **Open http://localhost:3000** in your browser

3. **Check the chat interface:**
   - You should see a dev mode banner: "🔧 DEV MODE - Authenticated as: john.doe@dept.gov"
   - Type a message and see streaming responses from Ollama
   - Messages should have good contrast (dark text on light background)

4. **Test backend directly:**
   ```bash
   curl http://localhost:8000/health
   ```

## 📁 Project Structure

```
/
├── host-site/              # Test harness - department landing page (port 3000)
│   ├── index.html          # Static HTML with iframe embed
│   ├── styles.css          # Department branding
│   └── server.js           # Optional Express server (Python http.server also works)
│
├── frontend/               # Next.js chat/workflow UI (port 3001)
│   ├── app/
│   │   ├── page.tsx        # Main chat interface with streaming
│   │   ├── layout.tsx      # App layout
│   │   └── globals.css     # Tailwind styles
│   ├── components/         # React components (future)
│   ├── lib/                # API clients, utilities (future)
│   └── public/
│       └── embed.js        # Portable embedding script (future)
│
├── backend/                # FastAPI + LangGraph backend (port 8000)
│   ├── app/
│   │   ├── main.py         # FastAPI app with CORS, health endpoints
│   │   ├── chat.py         # Streaming chat endpoint with Ollama
│   │   ├── auth/
│   │   │   └── middleware.py   # Dual-mode auth (cert/mock)
│   │   ├── workflows/      # LangGraph workflow definitions (future)
│   │   ├── mcp/            # MCP connector framework (future)
│   │   └── rag/            # RAG implementation with FAISS (future)
│   ├── db/                 # SQLite database and FAISS index (future)
│   ├── requirements.txt    # Python dependencies
│   └── pyproject.toml      # Python project metadata
│
├── mock-services/          # Development mocks (future)
│   ├── openai-mock/        # OpenAI-compatible API simulator
│   ├── enterprise-mocks/   # Jira/Confluence/SharePoint simulators
│   └── sample-data/        # Mock department docs, tickets, pages
│
├── docs/                   # Documentation
│   ├── images/             # Screenshots
│   ├── DEPLOYMENT.md       # Air-gapped deployment guide (future)
│   ├── EMBED_GUIDE.md      # Platform integration guide (future)
│   ├── ARCHITECTURE.md     # Detailed system design (future)
│   └── API.md              # Backend API reference (future)
│
├── .env.example            # Environment variables template
├── .env                    # Local configuration (git-ignored)
├── .venv/                  # Python virtual environment (git-ignored)
├── PLAN.md                 # Detailed implementation plan
└── README.md               # This file
```

## 🎨 Key Features

### ✅ Currently Implemented

- **Streaming Chat with Ollama**: Real-time AI responses using local llama3 model
- **Mock Authentication**: Development mode with X-Mock-User header simulation
- **Dynamic Theming**: URL parameters + postMessage for visual integration
- **iframe Security**: CORS, CSP headers, origin validation
- **Three-Server Architecture**: Isolated host, frontend, backend services
- **Hot Reload Development**: Fast iteration with Next.js and Uvicorn
- **Server-Sent Events (SSE)**: Efficient streaming from backend to frontend

### 🚧 Planned Features

- **RAG Documentation Q&A**: FAISS vector store for department knowledge base
- **LangGraph Workflows**: Multi-step agentic tasks with state management
- **MCP Connectors**: Direct integration with Jira, Confluence, SharePoint
- **SQLite Persistence**: Chat history and workflow state storage
- **Client Certificate Auth**: Production X.509 certificate validation
- **Docker Compose Deployment**: Single-command air-gapped deployment
- **Portable Embed Script**: Zero-config embedding for any platform

## 📸 Screenshots

### Department Landing Page with Embedded Chat
*The host site (port 3000) embedding the AI chat interface via iframe*

> **Screenshot Placeholder**: Department landing page with blue header "🏛️ Department of Technology", navigation menu, and embedded chat iframe showing the AI assistant with dev mode banner.

### Chat Interface with Ollama Streaming
*Real-time streaming responses from the local llama3 model*

> **Screenshot Placeholder**: Chat interface showing user messages (blue bubbles, right-aligned) and AI responses (gray bubbles, left-aligned) with proper text contrast. Header shows "🤖 AI Assistant - Powered by Ollama (llama3:latest)".

### Dynamic Theme Integration
*Theme parameters passed via URL for seamless visual integration*

```html
<!-- Example: Corporate blue theme with mock user -->
<iframe src="http://localhost:3001?theme=corporate-blue&mockUser=john.doe@dept.gov">
</iframe>
```

## 🔧 Technology Stack

### Frontend
- **Next.js 16.1.3** - React framework with app router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Server-Sent Events (SSE)** - Streaming responses

### Backend
- **FastAPI 0.115.0** - Modern Python web framework
- **Uvicorn** - ASGI server with hot reload
- **Pydantic 2.9** - Data validation
- **PyJWT 2.9** - JWT token handling
- **OpenAI Python SDK 1.57** - Ollama API client

### AI & Data
- **Ollama** - Local LLM runtime (llama3:latest)
- **SQLite** - Chat history (planned)
- **FAISS** - Vector similarity search (planned)

### Infrastructure
- **Python 3.11+** - Backend runtime
- **Node.js 18+** - Frontend build toolchain
- **Virtual Environment** - Isolated Python dependencies

## 🔐 Development Mode Features

```
/
├── host-site/              # Test harness - department landing page (port 3000)
├── frontend/               # Next.js chat/workflow UI (port 3001)
├── backend/                # FastAPI + LangGraph backend (port 8000)
│   ├── app/
│   │   ├── main.py         # FastAPI app with health/config endpoints
│   │   ├── auth/           # Authentication middleware
│   │   ├── workflows/      # LangGraph workflow definitions
│   │   ├── mcp/            # MCP connector framework
│   │   └── rag/            # RAG implementation with FAISS
│   └── db/                 # SQLite database and FAISS index
├── mock-services/          # Development mocks (OpenAI, Jira, etc.)
├── docs/                   # Documentation
├── .env.example            # Environment variables template
└── README.md               # This file
```

## � Development Mode Features

### Mock Authentication

The system supports dual-mode authentication:

- **Development Mode:** Pass `?mockUser=username@dept.gov` in URL or `X-Mock-User` header
- **Production Mode:** Client certificate (X.509) validation with JWT generation (planned)

Example iframe URL with mock user:
```html
<iframe src="http://localhost:3001?theme=corporate-blue&mockUser=john.doe@dept.gov">
</iframe>
```

### Theme Customization

The frontend supports dynamic theming via URL parameters:

- `?theme=corporate-blue` - Preset theme (navy blue #003366)
- `?primary=#003366&secondary=#0066cc` - Custom colors (planned)

Themes can also be passed via postMessage from parent window:

```javascript
iframe.contentWindow.postMessage({
  type: 'theme',
  primary: '#003366',
  secondary: '#0066cc',
  background: '#f5f5f5',
  font: 'Arial, sans-serif'
}, 'http://localhost:3001');
```

## 🔌 API Endpoints

### Backend (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info and available endpoints |
| `/health` | GET | Health check with auth mode and service status |
| `/api/config` | GET | Current configuration (safe subset) |
| `/api/chat/stream` | POST | Streaming chat with SSE |
| `/api/chat/` | POST | Non-streaming chat completion (planned) |

### Example: Streaming Chat Request

```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-Mock-User: john.doe@dept.gov" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is quantum computing?"}
    ],
    "stream": true
  }'
```

Response (Server-Sent Events):
```
data: Quantum
data:  computing
data:  is
data:  a
data:  revolutionary
data: [DONE]
```

## 🐳 Docker Compose (Coming Soon)

Single-command startup:
```bash
docker-compose up
```

## 📚 Next Steps

### ✅ Completed (MVP Phase 1)
- [x] Project scaffolding with three-server architecture
- [x] Next.js frontend with dynamic theming
- [x] FastAPI backend with CORS and auth middleware  
- [x] Ollama integration with streaming chat
- [x] Mock authentication (X-Mock-User header)
- [x] Server-Sent Events for real-time responses
- [x] iframe embedding with security controls
- [x] Development environment with hot reload

### 🎯 Next Phase (MVP Phase 2)
- [ ] SQLite persistence for chat history
- [ ] Session management with user isolation
- [ ] RAG implementation with FAISS vector store
- [ ] Sample department documentation for RAG
- [ ] LangGraph workflow engine integration
- [ ] Example workflow: "Create Jira ticket from chat"
- [ ] MCP connector base classes
- [ ] Mock services for Jira/Confluence/SharePoint

### 🚀 Future Enhancements
- [ ] Production client certificate authentication
- [ ] Docker Compose deployment configuration
- [ ] Portable embed.js script for zero-config embedding
- [ ] WordPress/SharePoint/Confluence integration guides
- [ ] Air-gapped deployment documentation
- [ ] Multi-department tenancy with data isolation
- [ ] Workflow state persistence and resumption
- [ ] Admin dashboard for monitoring

## 📊 Current Status

**Project Phase:** MVP - Core Chat Working  
**Latest Update:** January 17, 2026  
**Test Coverage:** Manual testing only  
**Deployment:** Local development only

### Working Features:
✅ Live chat with Ollama llama3 model  
✅ Streaming responses via SSE  
✅ Mock user authentication  
✅ Dynamic theme application  
✅ iframe embedding

### Known Limitations:
⚠️ No chat history persistence  
⚠️ No RAG/document search yet  
⚠️ No workflow execution  
⚠️ Development mode only (no cert auth)  
⚠️ No Docker deployment yet

## 📖 Documentation

- **[PLAN.md](PLAN.md)** - Complete implementation plan with 13 steps
- **[.env.example](.env.example)** - Environment configuration template
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system design *(planned)*
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Air-gapped deployment guide *(planned)*
- **[EMBED_GUIDE.md](docs/EMBED_GUIDE.md)** - Platform integration guide *(planned)*
- **[API.md](docs/API.md)** - Backend API reference *(planned)*

## 🛠️ Troubleshooting

**Port already in use:**
```bash
# Kill process on port 3000, 3001, or 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:3001 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Ollama connection failed:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama if needed (macOS)
ollama serve

# Test Ollama API
curl http://localhost:11434/api/tags
```

**Python module not found:**
```bash
# Ensure PYTHONPATH is set when running uvicorn
cd backend
PYTHONPATH=$PWD python -m uvicorn app.main:app --reload --port 8000
```

**Frontend not updating:**
```bash
# Hard refresh browser
# Mac: Cmd + Shift + R
# Windows/Linux: Ctrl + Shift + R

# Or restart Next.js dev server
cd frontend
rm -rf .next
npm run dev
```

**Backend CORS errors:**
- Check that ALLOWED_ORIGINS in `.env` includes your frontend URL
- Verify CORS middleware in `backend/app/main.py`

## 🤝 Contributing

This is an internal department project. For questions or issues:

1. Check existing documentation in `PLAN.md` and `README.md`
2. Review terminal output for error messages
3. Test with curl commands to isolate frontend vs backend issues
4. Check browser console for JavaScript errors

## 📝 Environment Variables

Key configuration in `.env`:

```bash
# Service URLs
FRONTEND_URL=http://localhost:3001
BACKEND_URL=http://localhost:8000

# Ollama Configuration
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3:latest

# Development Auth
ENVIRONMENT=development
DEFAULT_MOCK_USER=john.doe@dept.gov
JWT_SECRET_KEY=dev-secret-key-change-in-production
```

See [.env.example](.env.example) for complete configuration options.

## 🔒 Security Notes

⚠️ **Development Mode Only** - Current implementation:
- Uses mock authentication (X-Mock-User header)
- JWT secret is hardcoded for development
- CORS allows localhost only
- No rate limiting or input validation beyond Pydantic

🔐 **For Production:**
- Implement client certificate validation
- Rotate JWT secret keys
- Add rate limiting and request throttling
- Implement input sanitization and validation
- Enable CSP headers with strict directives
- Add audit logging for all AI interactions
- Implement data retention policies

## 📄 License

Internal use only. Department of Technology - 2026.

---

**Status:** 🟢 MVP Phase 1 Complete - Streaming Chat Working  
**Last Updated:** January 17, 2026  
**Next Milestone:** RAG Implementation + Chat Persistence
