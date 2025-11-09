# Testing MCP Server in VS Code

## Setup Complete! ✅

Your MCP server is now configured for VS Code. Here are the ways to test it:

## Method 1: GitHub Copilot Chat (Easiest)

**Requirements**: GitHub Copilot extension with Chat enabled

1. **Open Copilot Chat** (Ctrl+Shift+I or Cmd+Shift+I on Mac)

2. **Use the @ menu** to reference your MCP server:
   - Type `@` in the chat
   - Look for "map-demo-server" in the list of available MCP servers
   - Select it to use its tools and resources

3. **Try these commands**:
   ```
   @map-demo-server Get info about Tokyo
   ```
   ```
   @map-demo-server Find all cities in the USA
   ```
   ```
   @map-demo-server Calculate distance between London and Tokyo
   ```

## Method 2: MCP Inspector (Visual Testing)

**Already running!** The Inspector should be open at:
http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...

Or restart it:
```bash
npx @modelcontextprotocol/inspector venv/bin/python mcp_server.py
```

### What to Test in Inspector:

**Resources Tab**:
- `map://all-cities` - View all cities
- `map://city/London` - Get specific city data

**Tools Tab**:
- `find_cities_by_country` - Try: `{"country": "Japan"}`
- `get_city_info` - Try: `{"city_name": "San Francisco"}`
- `calculate_distance` - Try: `{"city1": "London", "city2": "Tokyo"}`

**Prompts Tab**:
- `city_report_prompt` - Try: `{"city_name": "Tokyo", "style": "tourist"}`

## Method 3: VS Code Tasks

Press `Cmd+Shift+P` and type "Tasks: Run Task", then select:
- **Start MCP Server** - Runs the server directly
- **Test with Inspector** - Launches MCP Inspector

## Method 4: Direct Python Testing

Create a test file and run it:

```python
# test_mcp_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    server_params = StdioServerParameters(
        command="venv/bin/python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])
            
            # Call a tool
            result = await session.call_tool("get_city_info", {"city_name": "Tokyo"})
            print("Tokyo info:", result.content[0].text)

asyncio.run(test_server())
```

## Debugging Tips

### Check if server is running:
```bash
# In terminal
ps aux | grep mcp_server.py
```

### View server logs:
The MCP Inspector terminal shows all server communication in real-time.

### Restart server:
Kill the inspector process (Ctrl+C) and rerun:
```bash
npx @modelcontextprotocol/inspector venv/bin/python mcp_server.py
```

## VS Code Configuration Files

- `.vscode/mcp-settings.json` - MCP server configuration
- `.vscode/settings.json` - Workspace settings with MCP enabled

## Next Steps

1. **Try it in Copilot Chat**: Open chat and use `@map-demo-server`
2. **Explore the Inspector**: Test all tools, resources, and prompts
3. **Extend the server**: Add more cities to `get_mock_map_data()`
4. **Integrate with Claude Desktop**: See MCP_README.md

## Troubleshooting

**Server not showing in Copilot Chat?**
- Make sure Copilot Chat is updated to the latest version
- Reload VS Code window (Cmd+Shift+P → "Developer: Reload Window")
- Check that `github.copilot.chat.mcp.enabled` is true in settings

**Inspector not working?**
- Ensure Node.js is installed: `node --version`
- Check that port 6274 is not in use
- Try with `DANGEROUSLY_OMIT_AUTH=true` environment variable

**Python errors?**
- Verify Python 3.11: `venv/bin/python --version`
- Reinstall dependencies: `venv/bin/pip install -r requirements.txt`
