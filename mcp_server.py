"""
MCP Demo Map Server

A Model Context Protocol server that exposes geographic data through MCP primitives.
This demonstrates how to convert a REST API into a proper MCP server.
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Create the MCP server
mcp = FastMCP(
    "MCP Demo Map Server",
    instructions="A demonstration MCP server providing mock geographic data in GeoJSON format. Use the tools to retrieve city information and the resources to access map data directly."
)

def get_mock_map_data() -> Dict[str, Any]:
    """
    Generate mock geographic/map data for demonstration.
    
    Returns:
        dict: A dictionary containing mock map features with coordinates and properties.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-122.4194, 37.7749]
                },
                "properties": {
                    "name": "San Francisco",
                    "population": 873965,
                    "country": "USA"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-0.1276, 51.5074]
                },
                "properties": {
                    "name": "London",
                    "population": 8982000,
                    "country": "UK"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [139.6917, 35.6895]
                },
                "properties": {
                    "name": "Tokyo",
                    "population": 13960000,
                    "country": "Japan"
                }
            }
        ]
    }


# MCP Resource: Expose map data as a resource
@mcp.resource("map://all-cities")
def get_all_cities_resource() -> str:
    """Get all cities as a GeoJSON FeatureCollection resource."""
    import json
    data = get_mock_map_data()
    return json.dumps(data, indent=2)


@mcp.resource("map://city/{city_name}")
def get_city_resource(city_name: str) -> str:
    """Get information about a specific city."""
    import json
    all_data = get_mock_map_data()
    
    # Find the city
    for feature in all_data["features"]:
        if feature["properties"]["name"].lower() == city_name.lower():
            return json.dumps(feature, indent=2)
    
    return json.dumps({"error": f"City '{city_name}' not found"})


# MCP Tool: Search for cities by country
@mcp.tool()
def find_cities_by_country(country: str) -> Dict[str, Any]:
    """
    Find all cities in a specific country.
    
    Args:
        country: The country name to filter by (e.g., "USA", "UK", "Japan")
    
    Returns:
        A GeoJSON FeatureCollection with cities from the specified country
    """
    all_data = get_mock_map_data()
    filtered_features = [
        f for f in all_data["features"] 
        if f["properties"]["country"].lower() == country.lower()
    ]
    
    return {
        "type": "FeatureCollection",
        "features": filtered_features,
        "count": len(filtered_features)
    }


# MCP Tool: Get city information
@mcp.tool()
def get_city_info(city_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific city.
    
    Args:
        city_name: The name of the city (e.g., "San Francisco", "London", "Tokyo")
    
    Returns:
        City information including coordinates, population, and country
    """
    all_data = get_mock_map_data()
    
    for feature in all_data["features"]:
        if feature["properties"]["name"].lower() == city_name.lower():
            return {
                "name": feature["properties"]["name"],
                "country": feature["properties"]["country"],
                "population": feature["properties"]["population"],
                "coordinates": {
                    "longitude": feature["geometry"]["coordinates"][0],
                    "latitude": feature["geometry"]["coordinates"][1]
                },
                "geometry_type": feature["geometry"]["type"]
            }
    
    return {"error": f"City '{city_name}' not found"}


# MCP Tool: Calculate distance between two cities (mock implementation)
@mcp.tool()
def calculate_distance(city1: str, city2: str) -> Dict[str, Any]:
    """
    Calculate the approximate distance between two cities.
    
    Args:
        city1: Name of the first city
        city2: Name of the second city
    
    Returns:
        Distance information in kilometers (simplified calculation)
    """
    all_data = get_mock_map_data()
    
    # Find both cities
    coords1 = None
    coords2 = None
    
    for feature in all_data["features"]:
        name = feature["properties"]["name"]
        if name.lower() == city1.lower():
            coords1 = feature["geometry"]["coordinates"]
        if name.lower() == city2.lower():
            coords2 = feature["geometry"]["coordinates"]
    
    if not coords1:
        return {"error": f"City '{city1}' not found"}
    if not coords2:
        return {"error": f"City '{city2}' not found"}
    
    # Simple distance calculation (not accurate, just for demo)
    # In a real app, you'd use the Haversine formula
    import math
    lon1, lat1 = coords1
    lon2, lat2 = coords2
    
    # Rough approximation
    dx = (lon2 - lon1) * 111  # degrees to km (longitude)
    dy = (lat2 - lat1) * 111  # degrees to km (latitude)
    distance = math.sqrt(dx*dx + dy*dy)
    
    return {
        "city1": city1,
        "city2": city2,
        "distance_km": round(distance, 2),
        "note": "This is a simplified calculation for demonstration purposes"
    }


# MCP Prompt: Generate a city report
@mcp.prompt()
def city_report_prompt(city_name: str, style: str = "detailed") -> str:
    """
    Generate a prompt for creating a city report.
    
    Args:
        city_name: The name of the city to report on
        style: Report style - "brief", "detailed", or "tourist"
    """
    styles = {
        "brief": "Please provide a brief one-paragraph summary about",
        "detailed": "Please provide a comprehensive report covering history, culture, economy, and key attractions of",
        "tourist": "Please create a tourist guide highlighting the must-see attractions, local cuisine, and travel tips for"
    }
    
    prompt_text = styles.get(style, styles["detailed"])
    return f"{prompt_text} {city_name}. Include relevant geographic and demographic information."


if __name__ == "__main__":
    # Run the MCP server using stdio transport (for Claude Desktop integration)
    mcp.run()
