from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EchoArguments(BaseModel):
    text: str = Field(..., min_length=1, description="Text to echo back to the client")
    prefix: Optional[str] = Field(
        None,
        description="Optional prefix to prepend before the echoed text",
    )


class SummarizeArguments(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    max_words: int = Field(12, ge=1, le=40, description="Maximum number of words to include")


class ToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]


class ToolCallError(Exception):
    def __init__(self, message: str, code: int = -32001):
        self.message = message
        self.code = code
        super().__init__(message)


def _echo_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        name="echo",
        description="Echoes the provided text back to the caller.",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to echo"},
                "prefix": {"type": "string", "description": "Optional prefix"},
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    )


def _summarize_tool_definition() -> ToolDefinition:
    return ToolDefinition(
        name="summarize",
        description="Returns a short summary of the supplied text.",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to summarize"},
                "max_words": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 40,
                    "description": "Maximum number of words in the summary",
                },
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    )


TOOL_REGISTRY: Dict[str, ToolDefinition] = {
    "echo": _echo_tool_definition(),
    "summarize": _summarize_tool_definition(),
}


def list_tools() -> List[ToolDefinition]:
    return list(TOOL_REGISTRY.values())


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool_name == "echo":
        parsed = EchoArguments.model_validate(arguments)
        prefix = parsed.prefix or ""
        text = f"{prefix}{parsed.text}" if prefix else parsed.text
        return {"content": [{"type": "text", "text": text}]}

    if tool_name == "summarize":
        parsed = SummarizeArguments.model_validate(arguments)
        words = parsed.text.split()
        max_words = min(parsed.max_words, len(words))
        summary = " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")
        return {"content": [{"type": "text", "text": summary}]}

    raise ToolCallError(f"Tool '{tool_name}' is not available", code=-32001)
