from fastapi import APIRouter, HTTPException

from app.schemas.mcp import MCPRequest, MCPResponse
from app.services.mcp_registry import ToolCallError, execute_tool, list_tools

router = APIRouter()


@router.post("")
async def handle_mcp(request: MCPRequest) -> MCPResponse:
    """Handle a minimal JSON-RPC-style MCP endpoint with initialize/list/call methods."""
    if request.method == "initialize":
        return MCPResponse(
            id=request.id,
            result={
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "llm-mcp-server", "version": "0.1.0"},
                "capabilities": {"tools": {"listChanged": False}},
            },
        )

    if request.method == "tools/list":
        return MCPResponse(
            id=request.id,
            result={"tools": [tool.model_dump() for tool in list_tools()]},
        )

    if request.method == "tools/call":
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        if not isinstance(tool_name, str) or not tool_name.strip():
            raise HTTPException(status_code=400, detail="A tool name is required")

        try:
            result = execute_tool(tool_name, arguments or {})
        except ToolCallError as exc:
            return MCPResponse(
                id=request.id,
                error={"code": exc.code, "message": exc.message},
            )
        except ValueError as exc:
            return MCPResponse(
                id=request.id,
                error={"code": -32602, "message": str(exc)},
            )

        return MCPResponse(id=request.id, result=result)

    return MCPResponse(id=request.id, error={"code": -32601, "message": "Method not found"})
