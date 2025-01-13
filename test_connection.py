import asyncio
import json
import sys
from mcp.client.stdio import StdioClientTransport
from mcp.client.client import Client

async def test_connection():
    # Create client and connect
    transport = StdioClientTransport('python3 -m notion_api_mcp')
    client = Client()
    await client.connect(transport)
    
    try:
        # Initialize connection
        init_response = await client.initialize(
            protocol_version="0.1.0",
            capabilities={},
            client_info={
                "name": "test-client",
                "version": "1.0.0"
            }
        )
        print("Initialization response:", json.dumps(init_response, indent=2))
        
        # Call verify_connection tool
        response = await client.call_tool("verify_connection", {})
        print("\nVerify connection response:", json.dumps(response, indent=2))
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())