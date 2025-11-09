# MCP Server Setup and Testing

This branch demonstrates a full **Model Context Protocol (MCP)** server implementation using the official MCP Python SDK.

## What Changed from main branch?

The main branch has a simple Flask REST API. This branch converts it to a **proper MCP server** that:

- ✅ Exposes **Resources** (map data accessible to LLM context)
- ✅ Provides **Tools** (functions the LLM can call)
- ✅ Defines **Prompts** (reusable templates for interactions)

## Requirements

- **Python 3.10+** (The MCP SDK requires Python 3.10 or newer)
- Node.js and npx (for MCP Inspector)

## Setup

```bash
# Create virtual environment with Python 3.11+
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Testing with MCP Inspector

The **MCP Inspector** is an official tool from Anthropic that provides a visual playground UI for testing MCP servers.

### Install and Run Inspector

```bash
# Test your MCP server with the inspector
npx @modelcontextprotocol/inspector venv/bin/python mcp_server.py
```

This will:
1. Start your MCP server
2. Launch the Inspector UI in your browser (usually at http://localhost:5173)
3. Let you interactively test:
   - **Resources**: `map://all-cities`, `map://city/{city_name}`
   - **Tools**: `find_cities_by_country`, `get_city_info`, `calculate_distance`
   - **Prompts**: `city_report_prompt`

### What You'll See in the Inspector

**Resources Tab**:
- Browse available map data
- Click on `map://all-cities` to see all cities in GeoJSON format
- Try `map://city/London` to get data for a specific city

**Tools Tab**:
- **find_cities_by_country**: Filter cities by country (try "USA")
- **get_city_info**: Get detailed info about a city (try "Tokyo")
- **calculate_distance**: Calculate distance between two cities

**Prompts Tab**:
- **city_report_prompt**: Generate prompts for city reports with different styles (brief/detailed/tourist)

## MCP Server Features

### Resources (Data Exposure)
```
map://all-cities          - All cities in GeoJSON format
map://city/{city_name}    - Specific city data
```

### Tools (LLM-callable Functions)
```python
find_cities_by_country(country: str) -> GeoJSON with filtered cities
get_city_info(city_name: str) -> City details with coordinates
calculate_distance(city1: str, city2: str) -> Distance in km
```

### Prompts (Templates)
```python
city_report_prompt(city_name: str, style: str) -> Formatted prompt
```

## Integrating with Claude Desktop

Once tested, you can integrate this server with Claude Desktop:

```bash
# Add to Claude Desktop configuration
npx @modelcontextprotocol/inspector install venv/bin/python mcp_server.py
```

Or manually add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "map-server": {
      "command": "/Users/micheal/Projects/mcp/Mcpdemo/venv/bin/python",
      "args": ["/Users/micheal/Projects/mcp/Mcpdemo/mcp_server.py"]
    }
  }
}
```

## Architecture Comparison

### Old (Flask REST API)
```
Client → HTTP GET /map → Server → JSON Response
```

### New (MCP Server)
```
LLM Client ← MCP Protocol → Server
     ├── Read Resources (passive data)
     ├── Call Tools (active functions)
     └── Use Prompts (templates)
```

## Development

The MCP server (`mcp_server.py`) maintains the same mock data as `app.py` but exposes it through MCP primitives instead of REST endpoints.

**Key Files**:
- `mcp_server.py` - MCP server implementation
- `app.py` - Original Flask REST API (still functional)
- `requirements.txt` - Now includes `mcp[cli]` package

## Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://modelcontextprotocol.io/specification/latest)
