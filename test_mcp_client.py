"""
Simple test script to verify MCP server is working correctly.
Run this in VS Code to test the MCP server without the inspector.
"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl


async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🚀 Testing MCP Demo Map Server...\n")
    
    # Configure server parameters
    server_params = StdioServerParameters(
        command="venv/bin/python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            print("📡 Initializing connection...")
            await session.initialize()
            print("✅ Connected!\n")
            
            # Test 1: List Resources
            print("=" * 50)
            print("TEST 1: Listing Resources")
            print("=" * 50)
            resources = await session.list_resources()
            print(f"Found {len(resources.resources)} resources:")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            print()
            
            # Test 2: Read a Resource
            print("=" * 50)
            print("TEST 2: Reading Resource 'map://all-cities'")
            print("=" * 50)
            content = await session.read_resource(AnyUrl("map://all-cities"))
            print(f"Content preview: {content.contents[0].text[:200]}...")
            print()
            
            # Test 3: List Tools
            print("=" * 50)
            print("TEST 3: Listing Tools")
            print("=" * 50)
            tools = await session.list_tools()
            print(f"Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Test 4: Call a Tool - Get City Info
            print("=" * 50)
            print("TEST 4: Calling Tool 'get_city_info'")
            print("=" * 50)
            result = await session.call_tool("get_city_info", {"city_name": "Tokyo"})
            print(f"Result: {result.content[0].text}")
            if result.structuredContent:
                print(f"Structured data: {result.structuredContent}")
            print()
            
            # Test 5: Call a Tool - Find Cities by Country
            print("=" * 50)
            print("TEST 5: Calling Tool 'find_cities_by_country'")
            print("=" * 50)
            result = await session.call_tool("find_cities_by_country", {"country": "USA"})
            print(f"Result: {result.content[0].text}")
            print()
            
            # Test 6: Call a Tool - Calculate Distance
            print("=" * 50)
            print("TEST 6: Calling Tool 'calculate_distance'")
            print("=" * 50)
            result = await session.call_tool(
                "calculate_distance", 
                {"city1": "London", "city2": "Tokyo"}
            )
            print(f"Result: {result.content[0].text}")
            print()
            
            # Test 7: List Prompts
            print("=" * 50)
            print("TEST 7: Listing Prompts")
            print("=" * 50)
            prompts = await session.list_prompts()
            print(f"Found {len(prompts.prompts)} prompts:")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            print()
            
            # Test 8: Get a Prompt
            print("=" * 50)
            print("TEST 8: Getting Prompt 'city_report_prompt'")
            print("=" * 50)
            prompt_result = await session.get_prompt(
                "city_report_prompt",
                {"city_name": "San Francisco", "style": "tourist"}
            )
            print(f"Prompt text: {prompt_result.messages[0].content.text}")
            print()
            
            print("=" * 50)
            print("🎉 All tests passed!")
            print("=" * 50)


if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
