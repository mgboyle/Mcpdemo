"""
MCP Demo Map Server

A simple Flask-based map server demonstrating MCP (Model Context Protocol) concepts.
This server provides mock geographic data endpoints for demonstration purposes.
"""

from flask import Flask, jsonify
from typing import Dict, Any

app = Flask(__name__)


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


@app.route('/ping', methods=['GET'])
def ping() -> tuple[Dict[str, str], int]:
    """
    Health check endpoint.
    
    Returns:
        tuple: A JSON response with status and message, and HTTP status code 200.
    """
    return jsonify({
        "status": "ok",
        "message": "MCP Demo Map Server is running"
    }), 200


@app.route('/map', methods=['GET'])
def map_data() -> tuple[Dict[str, Any], int]:
    """
    Map data endpoint returning mock geographic features.
    
    Returns:
        tuple: A JSON response with GeoJSON-formatted mock data, and HTTP status code 200.
    """
    data = get_mock_map_data()
    return jsonify(data), 200


@app.route('/', methods=['GET'])
def root() -> tuple[Dict[str, Any], int]:
    """
    Root endpoint providing API information.
    
    Returns:
        tuple: A JSON response with API details and available endpoints, and HTTP status code 200.
    """
    return jsonify({
        "name": "MCP Demo Map Server",
        "version": "1.0.0",
        "description": "A simple map server demonstrating MCP concepts with mock geographic data",
        "endpoints": {
            "/": "API information",
            "/ping": "Health check endpoint",
            "/map": "Get mock map data (GeoJSON format)"
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
