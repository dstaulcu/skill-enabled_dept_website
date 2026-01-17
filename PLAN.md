# Plan: AI-Enhanced Air-Gapped Department Website

Build a modern department website with integrated AI chat, MCP-enabled agentic workflows, and enterprise tool integrations (Jira, Confluence, SharePoint) using an internal OpenAI-compatible model service. Architecture: Next.js frontend + Python FastAPI/LangGraph backend for full Python ecosystem access in an air-gapped environment.

## Project Structure

```
/
├── host-site/              # Test harness - department landing page with iframe
│   ├── index.html          # Static page or Express server (port 3000)
│   ├── styles.css          # Department branding/theme
│   └── package.json        # Optional: if using Express
├── frontend/               # Next.js chat/workflow UI (port 3001)
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   │   └── embed.js        # Portable embedding script
│   └── package.json
├── backend/                # FastAPI + LangGraph (port 8000)
│   ├── app/
│   │   ├── main.py
│   │   ├── auth/
│   │   ├── workflows/
│   │   ├── mcp/
│   │   └── rag/
│   ├── db/
│   ├── requirements.txt
│   └── pyproject.toml
├── mock-services/          # Development mocks (bundled with backend or separate)
│   ├── openai-mock/        # OpenAI-compatible API
│   ├── enterprise-mocks/   # Jira/Confluence/SharePoint simulators
│   └── sample-data/        # Mock department docs, tickets, pages
├── docs/                   # Documentation
│   ├── DEPLOYMENT.md
│   ├── EMBED_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── API.md
├── docker-compose.yml      # Optional: orchestrate all services
├── .env.example            # Shared environment variables template
└── README.md               # Quick start guide
```

## Steps

1. **Create test harness and project scaffolding** by setting up three-server development environment: `host-site/` (static server or Express on port 3000 serving department landing page with iframe), `frontend/` (Next.js on port 3001), and `backend/` (FastAPI on port 8000). Initialize with shared `.env.example` defining `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`, service URLs, and mock authentication settings.

2. **Initialize dual-service architecture** by creating Next.js 14+ frontend in `frontend/` and Python FastAPI backend in `backend/` with proper TypeScript/Python tooling and dependency management.

3. **Build FastAPI backend with LangGraph** in `backend/app/` including `main.py` for API routes, `workflows/` for LangGraph definitions, `mcp/` for MCP server integrations, and `auth/middleware.py` for dual-mode authentication (production: client certificate validation and JWT generation; development: mock user identity via X-Mock-User header/query param) with identity propagation to all AI/MCP calls.

4. **Create Cline-to-LangGraph migration utilities** in `backend/workflows/converter.py` that parse Cline markdown workflow files and generate LangGraph StateGraph definitions with nodes, edges, and state schemas automatically.

5. **Implement MCP connector framework** in `backend/mcp/connectors/` with base classes and specific implementations for Jira, Confluence, and SharePoint that use propagated user credentials for scoped, role-based queries.

6. **Build Next.js frontend** replicating the department webpage screenshot in `frontend/app/page.tsx` with `components/AIChat.tsx` for streaming chat, `components/WorkflowPanel.tsx` for workflow execution with real-time step visibility, and FastAPI backend integration via `lib/api-client.ts`.

7. **Create portable embed system** with dynamic theming in `frontend/public/embed.js` that auto-generates iframes with URL-based theme parameters, supports auto-detection of parent page styles via postMessage, and provides preset configurations for common platforms (WordPress, SharePoint, Confluence) enabling zero-config deployment across diverse web frameworks.

8. **Implement RAG for documentation Q&A** in `backend/rag/` using LangChain document loaders, FAISS vector store for offline similarity search, and retrieval chains integrated into chat endpoint for site content questions.

9. **Build data persistence layer** in `backend/db/` with SQLite for chat history (session-scoped, department-scoped isolation), workflow state management (resumable long-running tasks), and multi-tenancy support with department/user segmentation ensuring data residency compliance and proper isolation. Schema designed for future PostgreSQL migration if needed.

10. **Implement iframe security framework** in `frontend/lib/iframe-security.ts` with CORS configuration, CSP headers, postMessage validation (origin checking, message signing), and XSS protection to ensure safe embedding across diverse platforms while maintaining security posture.

11. **Build mock services for local development** in `mock-services/` including `openai-mock/` (OpenAI-compatible API with local model or canned responses), `enterprise-mocks/` (Jira/Confluence/SharePoint API simulators with sample data), and certificate auth simulator that accepts mock user identities (`?mockUser=john.doe@dept.gov` or `X-Mock-User` header) and generates identical JWT structure as production certificate-based auth, enabling full-stack development and testing without enterprise dependencies, air-gapped infrastructure, or client certificates.

12. **Create sample data and seed content** in `mock-services/sample-data/` including mock department documentation (markdown files for RAG indexing), sample Jira tickets/projects, Confluence pages/spaces, SharePoint documents/lists, and example Cline workflow definitions for testing LangGraph migration and end-to-end workflow execution.

13. **Create comprehensive documentation** in `docs/` including `DEPLOYMENT.md` (air-gapped installation runbooks), `EMBED_GUIDE.md` (department onboarding with platform-specific examples), `ARCHITECTURE.md` (system design and data flows), and `API.md` (backend endpoints and integration specs) to support deployment, operations, and future development.

## Further Considerations

1. **Service communication**: Use HTTP REST between Next.js and FastAPI, or add WebSocket support in FastAPI for real-time workflow progress streaming? WebSocket recommended for better UX during long-running workflows.

2. **Development workflow**: Local development requires three services running simultaneously. Options: (1) Three terminal windows with manual startup, (2) Docker Compose with `docker-compose up` single command, (3) npm scripts with `concurrently` package. Recommend Docker Compose for POC to mirror production deployment, with documented manual startup as fallback.

3. **Vector database choice**: FAISS recommended for POC (file-based, fastest, minimal setup, perfect for air-gapped). Design allows future migration to Chroma (if frequent doc updates needed) or PGVector (if PostgreSQL adopted for multi-tenancy).

4. **Deployment packaging**: Docker recommended for air-gapped deployment with all dependencies pre-bundled and easier installation on isolated systems.

5. **Multi-platform theming strategy**: Embed system uses URL parameters for theme injection (primary color, fonts, backgrounds) with three-tier fallback: (1) postMessage auto-detection of parent styles, (2) URL parameter overrides, (3) default theme. Supports preset configurations (`?theme=corporate-blue`) for instant deployment across WordPress, SharePoint, Confluence, or custom frameworks without platform-specific code.

6. **Mock service implementation**: For local development, should mock services use static JSON responses or lightweight LLMs (Ollama, llama.cpp)? Static responses faster for UI development; local LLM provides realistic AI interactions. Recommend hybrid: static mocks for enterprise APIs, optional local LLM for OpenAI endpoint with fallback to canned responses.

7. **Authentication modes**: Production uses client certificate (X.509) presented to host site, extracted identity (CN, email) passed to iframe, validated and converted to JWT by backend. Development mode accepts mock identity via `X-Mock-User` header or `?mockUser=` query param, generates identical JWT structure. Both modes use same identity propagation flow to AI/MCP services. Include visual indicator (banner/badge) when running in dev auth mode.

8. **Data persistence strategy**: SQLite recommended for POC (zero setup, single file, fast, simple backup). Design schema for future PostgreSQL migration if multi-department scale requires row-level security and concurrent access. Chat history retention policy: session-only, 30-day, or indefinite with user consent?

9. **Security implementation**: Iframe sandbox attributes (allow-scripts, allow-same-origin), CSP directives for parent/child communication, postMessage allowlist for trusted origins. Data residency: all chat/workflow data stored locally in air-gapped environment with department-level isolation ensuring compliance with data governance policies.

## Technology Stack

- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with LangGraph
- **AI Model Service**: Internal OpenAI-compatible endpoint (air-gapped)
- **Workflow Engine**: LangGraph (Python)
- **MCP Integration**: Pre-staged MCP servers for enterprise tools
- **Authentication**: Client certificate (production), mock user header/param (development), JWT-based identity propagation
- **RAG/Vector Store**: FAISS for offline documentation Q&A
- **Data Persistence**: SQLite (designed for PostgreSQL migration path)
- **Security**: CSP headers, iframe sandboxing, postMessage validation
- **Deployment**: Docker Compose (recommended for air-gapped)
- **Development Mocks**: Express/FastAPI mock servers for OpenAI API, Jira, Confluence, SharePoint, and auth services
- **Documentation**: Markdown docs for deployment, embedding, architecture, and API reference

## Key Features

- ✅ Air-gapped compatible (no internet dependency)
- ✅ OpenAI-compatible internal model service
- ✅ Client certificate authentication (production) with dev mode simulation
- ✅ Identity propagation to all AI/MCP calls
- ✅ Real-time workflow step visibility
- ✅ Documentation Q&A with RAG
- ✅ Enterprise tool integrations (Jira, Confluence, SharePoint)
- ✅ Cline workflow migration support
- ✅ Role-based access control
- ✅ Platform-agnostic embed system (WordPress, SharePoint, Confluence, static sites)
- ✅ Dynamic theme adaptation via URL parameters and auto-detection
- ✅ Zero-config deployment with preset configurations
- ✅ Local development mock services (no enterprise dependencies required)
- ✅ Multi-tenant data isolation with department-level segmentation
- ✅ Chat history and workflow state persistence with resumable tasks
- ✅ Iframe security (CSP, CORS, postMessage validation, sandboxing)
- ✅ Data residency compliance (all data stored in air-gapped environment)
- ✅ Comprehensive deployment and integration documentation
