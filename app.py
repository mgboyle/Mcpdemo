"""
MCP Demo Map Server

A simple Flask-based map server demonstrating MCP (Model Context Protocol) concepts.
This server provides mock geographic data endpoints for demonstration purposes.
"""

from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from typing import Dict, Any

app = Flask(__name__)

# Configure Swagger UI
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "info": {
        "title": "MCP Demo Map Server API",
        "description": "A simple map server demonstrating MCP concepts with mock geographic data",
        "version": "1.0.0"
    },
    "schemes": ["http"],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)


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
    ---
    tags:
      - Health
    responses:
      200:
        description: Server is running
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            message:
              type: string
              example: MCP Demo Map Server is running
    """
    return jsonify({
        "status": "ok",
        "message": "MCP Demo Map Server is running"
    }), 200


@app.route('/map', methods=['GET'])
def map_data() -> tuple[Dict[str, Any], int]:
    """
    Map data endpoint returning mock geographic features.
    ---
    tags:
      - Map Data
    responses:
      200:
        description: GeoJSON formatted mock map data
        schema:
          type: object
          properties:
            type:
              type: string
              example: FeatureCollection
            features:
              type: array
              items:
                type: object
                properties:
                  type:
                    type: string
                    example: Feature
                  geometry:
                    type: object
                    properties:
                      type:
                        type: string
                        example: Point
                      coordinates:
                        type: array
                        items:
                          type: number
                        example: [-122.4194, 37.7749]
                  properties:
                    type: object
                    properties:
                      name:
                        type: string
                        example: San Francisco
                      population:
                        type: integer
                        example: 873965
                      country:
                        type: string
                        example: USA
    """
    data = get_mock_map_data()
    return jsonify(data), 200


@app.route('/', methods=['GET'])
def root() -> tuple[Dict[str, Any], int]:
    """
    Root endpoint providing API information.
    ---
    tags:
      - API Info
    responses:
      200:
        description: API information and available endpoints
        schema:
          type: object
          properties:
            name:
              type: string
              example: MCP Demo Map Server
            version:
              type: string
              example: 1.0.0
            description:
              type: string
              example: A simple map server demonstrating MCP concepts with mock geographic data
            endpoints:
              type: object
              properties:
                /:
                  type: string
                  example: API information
                /ping:
                  type: string
                  example: Health check endpoint
                /map:
                  type: string
                  example: Get mock map data (GeoJSON format)
                /apidocs/:
                  type: string
                  example: Interactive API documentation (Swagger UI)
    """
    return jsonify({
        "name": "MCP Demo Map Server",
        "version": "1.0.0",
        "description": "A simple map server demonstrating MCP concepts with mock geographic data",
        "endpoints": {
            "/": "API information",
            "/ping": "Health check endpoint",
            "/map": "Get mock map data (GeoJSON format)",
            "/apidocs/": "Interactive API documentation (Swagger UI)"
        }
    }), 200


if __name__ == '__main__':
    # Note: Debug mode is enabled for development/demonstration purposes only.
    # For production deployments, use a production WSGI server like gunicorn or waitress
    # and disable debug mode by setting debug=False or removing the parameter.
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    port = int(os.getenv('PORT', 5001))  # Changed default to 5001 to avoid macOS AirPlay conflict
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
