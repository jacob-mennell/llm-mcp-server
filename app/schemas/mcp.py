from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MCPRequest(BaseModel):
    jsonrpc: str = Field(default="2.0")
    id: Optional[int | str] = None
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[int | str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
