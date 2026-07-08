from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_initialize_returns_server_capabilities():
    response = client.post(
        "/v1/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {}},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["serverInfo"]["name"] == "llm-mcp-server"
    assert payload["result"]["capabilities"]["tools"]["listChanged"] is False


def test_tools_list_returns_registered_tools():
    response = client.post(
        "/v1/mcp",
        json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    )

    assert response.status_code == 200
    payload = response.json()
    tool_names = {tool["name"] for tool in payload["result"]["tools"]}
    assert {"echo", "summarize"}.issubset(tool_names)
    echo_tool = next(tool for tool in payload["result"]["tools"] if tool["name"] == "echo")
    assert echo_tool["inputSchema"]["properties"]["text"]["type"] == "string"


def test_tools_call_returns_content_payload():
    response = client.post(
        "/v1/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": "hello from the example server"}},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["content"][0]["type"] == "text"
    assert payload["result"]["content"][0]["text"] == "hello from the example server"


def test_unknown_tool_returns_jsonrpc_error():
    response = client.post(
        "/v1/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "does-not-exist", "arguments": {"text": "hello"}},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "error" in payload
    assert payload["error"]["code"] == -32001
