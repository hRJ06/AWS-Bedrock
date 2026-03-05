import os
from urllib.parse import urlparse

from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.multiagent.a2a import A2AServer
from strands.models import BedrockModel

EMPLOYEE_INFO_URL = "http://localhost:8002/mcp/"
EMPLOYEE_AGENT_URL = "http://localhost:8001/"

employee_mcp_client = MCPClient(
    lambda: streamable_http_client(EMPLOYEE_INFO_URL)
)

model = BedrockModel(
    model_id="us.anthropic.claude-3-haiku-20240307-v1:0",
    streaming=True
)

with employee_mcp_client:
    tools = employee_mcp_client.list_prompts_sync()
    print("Available MCP Tool - ")
    for tool in tools:
        print(f"    - {tool.tool_name}")
    print()

    employee_agent = Agent(
        model=model,
        name="Employee Agent",
        description="Answer question about employee.",
        tools=tools,
        system_prompt="You must abbreviate employee first name and list all their skill."
    )

    a2a_server = A2AServer(
        agent=employee_agent,
        host=urlparse(EMPLOYEE_AGENT_URL).hostname,
        port=int(urlparse(EMPLOYEE_AGENT_URL).port) 
    )

    if __name__ == "__main__":
        a2a_server.serve(host="0.0.0.0", port=8001)