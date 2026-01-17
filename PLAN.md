# Plan: AI-Enhanced Air-Gapped Department Website

Build a modern department website with integrated AI chat, MCP-enabled agentic workflows, and enterprise tool integrations (Jira, Confluence, SharePoint) using an internal OpenAI-compatible model service. Architecture: Next.js frontend + Python FastAPI/LangGraph backend for full Python ecosystem access in an air-gapped environment.

## Steps

1. **Initialize dual-service architecture** by creating Next.js 14+ frontend in `frontend/` and Python FastAPI backend in `backend/` with shared `.env.example` defining `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`, and service communication settings.

2. **Build FastAPI backend with LangGraph** in `backend/app/` including `main.py` for API routes, `workflows/` for LangGraph definitions, `mcp/` for MCP server integrations, and `auth/middleware.py` for JWT-based identity propagation to all AI/MCP calls.

3. **Create Cline-to-LangGraph migration utilities** in `backend/workflows/converter.py` that parse Cline markdown workflow files and generate LangGraph StateGraph definitions with nodes, edges, and state schemas automatically.

4. **Implement MCP connector framework** in `backend/mcp/connectors/` with base classes and specific implementations for Jira, Confluence, and SharePoint that use propagated user credentials for scoped, role-based queries.

5. **Build Next.js frontend** replicating the department webpage screenshot in `frontend/app/page.tsx` with `components/AIChat.tsx` for streaming chat, `components/WorkflowPanel.tsx` for workflow execution with real-time step visibility, and FastAPI backend integration via `lib/api-client.ts`.

6. **Create portable embed system** with dynamic theming in `frontend/public/embed.js` that auto-generates iframes with URL-based theme parameters, supports auto-detection of parent page styles via postMessage, and provides preset configurations for common platforms (WordPress, SharePoint, Confluence) enabling zero-config deployment across diverse web frameworks.

7. **Implement RAG for documentation Q&A** in `backend/rag/` using LangChain document loaders, vector store (Chroma or FAISS for offline use), and retrieval chains integrated into chat endpoint for site content questions.

8. **Build data persistence layer** in `backend/db/` with SQLite/PostgreSQL for chat history (session-scoped, department-scoped isolation), workflow state management (resumable long-running tasks), and multi-tenancy support with department/user segmentation ensuring data residency compliance and proper isolation.

9. **Implement iframe security framework** in `frontend/lib/iframe-security.ts` with CORS configuration, CSP headers, postMessage validation (origin checking, message signing), and XSS protection to ensure safe embedding across diverse platforms while maintaining security posture.

10. **Build mock services for local development** in `mock-services/` including `openai-mock/` (OpenAI-compatible API with local model or canned responses), `enterprise-mocks/` (Jira/Confluence/SharePoint API simulators with sample data), and `auth-mock/` (JWT token generation service) to enable full-stack development and testing without enterprise dependencies or air-gapped infrastructure.

11. **Create comprehensive documentation** in `docs/` including `DEPLOYMENT.md` (air-gapped installation runbooks), `EMBED_GUIDE.md` (department onboarding with platform-specific examples), `ARCHITECTURE.md` (system design and data flows), and `API.md` (backend endpoints and integration specs) to support deployment, operations, and future development.

## Further Considerations

1. **Service communication**: Use HTTP REST between Next.js and FastAPI, or add WebSocket support in FastAPI for real-time workflow progress streaming? WebSocket recommended for better UX during long-running workflows.

2. **Vector database choice**: FAISS (file-based, simpler) vs Chroma (persistent, better for updates) vs PGVector (requires PostgreSQL)? Air-gapped environment favors FAISS for simplicity unless you need frequent doc updates.

3. **Deployment packaging**: Should both services be containerized (Docker Compose) or deployed separately? Docker recommended for air-gapped deployment with all dependencies pre-bundled and easier installation on isolated systems.

4. **Multi-platform theming strategy**: Embed system uses URL parameters for theme injection (primary color, fonts, backgrounds) with three-tier fallback: (1) postMessage auto-detection of parent styles, (2) URL parameter overrides, (3) default theme. Supports preset configurations (`?theme=corporate-blue`) for instant deployment across WordPress, SharePoint, Confluence, or custom frameworks without platform-specific code.

5. **Mock service implementation**: For local development, should mock services use static JSON responses or lightweight LLMs (Ollama, llama.cpp)? Static responses faster for UI development; local LLM provides realistic AI interactions. Recommend hybrid: static mocks for enterprise APIs, optional local LLM for OpenAI endpoint with fallback to canned responses.

6. **Data persistence strategy**: SQLite for POC simplicity vs PostgreSQL for production multi-tenancy? SQLite sufficient for single-department POC; PostgreSQL required for row-level security and concurrent access across departments. Chat history retention policy: session-only, 30-day, or indefinite with user consent?

7. **Security implementation**: Iframe sandbox attributes (allow-scripts, allow-same-origin), CSP directives for parent/child communication, postMessage allowlist for trusted origins. Data residency: all chat/workflow data stored locally in air-gapped environment with department-level isolation ensuring compliance with data governance policies.

## Technology Stack

- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with LangGraph
- **AI Model Service**: Internal OpenAI-compatible endpoint (air-gapped)
- **Workflow Engine**: LangGraph (Python)
- **MCP Integration**: Pre-staged MCP servers for enterprise tools
- **Authentication**: JWT-based with identity propagation
- **RAG/Vector Store**: FAISS or Chroma for offline documentation Q&A
- **Data Persistence**: SQLite (POC) or PostgreSQL (production multi-tenancy)
- **Security**: CSP headers, iframe sandboxing, postMessage validation
- **Deployment**: Docker Compose (recommended for air-gapped)
- **Development Mocks**: Express/FastAPI mock servers for OpenAI API, Jira, Confluence, SharePoint, and auth services
- **Documentation**: Markdown docs for deployment, embedding, architecture, and API reference

## Key Features

- ✅ Air-gapped compatible (no internet dependency)
- ✅ OpenAI-compatible internal model service
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
