# Plan: AI-Enhanced Air-Gapped Department Website

Build a modern department website with integrated AI chat, MCP-enabled agentic workflows, and enterprise tool integrations (Jira, Confluence, SharePoint) using an internal OpenAI-compatible model service. Architecture: Next.js frontend + Python FastAPI/LangGraph backend for full Python ecosystem access in an air-gapped environment.

## Steps

1. **Initialize dual-service architecture** by creating Next.js 14+ frontend in `frontend/` and Python FastAPI backend in `backend/` with shared `.env.example` defining `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`, and service communication settings.

2. **Build FastAPI backend with LangGraph** in `backend/app/` including `main.py` for API routes, `workflows/` for LangGraph definitions, `mcp/` for MCP server integrations, and `auth/middleware.py` for JWT-based identity propagation to all AI/MCP calls.

3. **Create Cline-to-LangGraph migration utilities** in `backend/workflows/converter.py` that parse Cline markdown workflow files and generate LangGraph StateGraph definitions with nodes, edges, and state schemas automatically.

4. **Implement MCP connector framework** in `backend/mcp/connectors/` with base classes and specific implementations for Jira, Confluence, and SharePoint that use propagated user credentials for scoped, role-based queries.

5. **Build Next.js frontend** replicating the department webpage screenshot in `frontend/app/page.tsx` with `components/AIChat.tsx` for streaming chat, `components/WorkflowPanel.tsx` for workflow execution with real-time step visibility, and FastAPI backend integration via `lib/api-client.ts`.

6. **Implement RAG for documentation Q&A** in `backend/rag/` using LangChain document loaders, vector store (Chroma or FAISS for offline use), and retrieval chains integrated into chat endpoint for site content questions.

## Further Considerations

1. **Service communication**: Use HTTP REST between Next.js and FastAPI, or add WebSocket support in FastAPI for real-time workflow progress streaming? WebSocket recommended for better UX during long-running workflows.

2. **Vector database choice**: FAISS (file-based, simpler) vs Chroma (persistent, better for updates) vs PGVector (requires PostgreSQL)? Air-gapped environment favors FAISS for simplicity unless you need frequent doc updates.

3. **Deployment packaging**: Should both services be containerized (Docker Compose) or deployed separately? Docker recommended for air-gapped deployment with all dependencies pre-bundled and easier installation on isolated systems.

## Technology Stack

- **Frontend**: Next.js 14+ with TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with LangGraph
- **AI Model Service**: Internal OpenAI-compatible endpoint (air-gapped)
- **Workflow Engine**: LangGraph (Python)
- **MCP Integration**: Pre-staged MCP servers for enterprise tools
- **Authentication**: JWT-based with identity propagation
- **RAG/Vector Store**: FAISS or Chroma for offline documentation Q&A
- **Deployment**: Docker Compose (recommended for air-gapped)

## Key Features

- ✅ Air-gapped compatible (no internet dependency)
- ✅ OpenAI-compatible internal model service
- ✅ Identity propagation to all AI/MCP calls
- ✅ Real-time workflow step visibility
- ✅ Documentation Q&A with RAG
- ✅ Enterprise tool integrations (Jira, Confluence, SharePoint)
- ✅ Cline workflow migration support
- ✅ Role-based access control
