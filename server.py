from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from routes.items import app

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