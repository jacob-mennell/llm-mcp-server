# LLM MCP Server

This repository now works as a more protocol-faithful example MCP server built with FastAPI.
It demonstrates a minimal JSON-RPC-style MCP endpoint with tool registration, schema-driven arguments, and tool execution semantics that are closer to a real MCP server.

## What this example shows
- A FastAPI application with versioned routes.
- A lightweight authentication layer using an API key header.
- A JSON-RPC-style MCP endpoint at /v1/mcp.
- Registered tools with richer input schemas and validation.
- Two runnable example tools:
  - echo: returns the supplied text unchanged, with optional prefix support.
  - summarize: returns a short word-based summary with a configurable max_words parameter.
- A standard LLM endpoint at /v1/llm for prompt-based routing.
- Graceful fallback behavior when no real OpenAI key is configured, so the example still runs locally.

## Architecture
- app/main.py: application entrypoint and router registration.
- app/api/v1.py: the LLM endpoint.
- app/api/mcp.py: the example MCP-style tool endpoints.
- app/core/auth.py: API key validation.
- app/core/router.py: prompt routing logic.
- app/models/: provider-specific model adapters.
- tests/: end-to-end examples for the new behavior.

## Running locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv openai pytest httpx
   ```
3. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Send requests with the API key header:
   ```bash
   curl -X GET http://127.0.0.1:8000/v1/mcp/tools \
     -H "x-api-key: default-api-key"
   ```

## Example requests

### Initialize the server
```bash
curl -X POST http://127.0.0.1:8000/v1/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}'
```

### List available tools
```bash
curl -X POST http://127.0.0.1:8000/v1/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

### Execute the echo tool
```bash
curl -X POST http://127.0.0.1:8000/v1/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"echo","arguments":{"text":"hello from the example server"}}}'
```

### Execute the summarize tool
```bash
curl -X POST http://127.0.0.1:8000/v1/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"summarize","arguments":{"text":"This repository demonstrates a simple MCP-style tool server","max_words":8}}}'
```

### Call the LLM endpoint
```bash
curl -X POST http://127.0.0.1:8000/v1/llm \
  -H "x-api-key: default-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say hello!", "model": "gpt-4"}'
```

## Testing
Run the test suite with:
```bash
pytest -q
```

## Extending this example
You can extend this project by adding:
- new tools in app/api/mcp.py
- new model adapters in app/models/
- richer schemas and validation in app/schemas/
- additional auth or routing rules in app/core/

This repository is now suitable as a practical starting point for an example MCP server and as a foundation for a more complete implementation.
