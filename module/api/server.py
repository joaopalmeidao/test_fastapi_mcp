from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from .routes import items, agent

app = FastAPI(
    title="Example API",
    description="A simple example API with integrated MCP server",
    version="0.1.0",
)

app.include_router(items.router)
app.include_router(agent.router)

mcp = FastApiMCP(
    app,
    name="My API MCP",
    description="MCP server for the Item API",
    base_url="http://localhost:8000",
)

mcp.mount()

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host='0.0.0.0', port=8000)
