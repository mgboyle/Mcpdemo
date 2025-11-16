# MCP Demo Map Server

A lightweight Python Flask application demonstrating MCP (Model Context Protocol) concepts through a simple map server with mock geographic data.

## Overview

This "Hello World" style demo server provides RESTful API endpoints that return mock geographic data in GeoJSON format. It's designed to illustrate basic MCP server patterns with clean, modular code.

## Features

- **Simple Flask API** with three endpoints:
  - `GET /` - API information and available endpoints
  - `GET /ping` - Health check endpoint
  - `GET /map` - Returns mock geographic data in GeoJSON format
- **Mock Data** - Demonstrates geographic features without requiring real data sources
- **Clear Documentation** - Comprehensive docstrings and comments
- **Unit Tests** - pytest-based tests with mock responses
- **Lightweight** - Minimal dependencies, focused on clarity

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/mgboyle/Mcpdemo.git
   cd Mcpdemo
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the Flask development server:

```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see output similar to:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**Security Note:** Debug mode is enabled by default for development and demonstration purposes. For production use, disable debug mode by setting the environment variable:
```bash
FLASK_DEBUG=false python app.py
```
Or use a production WSGI server like gunicorn or waitress instead.

## API Endpoints

### GET /

Returns API information and available endpoints.

**Example:**
```bash
curl http://localhost:5000/
```

**Response:**
```json
{
  "name": "MCP Demo Map Server",
  "version": "1.0.0",
  "description": "A simple map server demonstrating MCP concepts with mock geographic data",
  "endpoints": {
    "/": "API information",
    "/ping": "Health check endpoint",
    "/map": "Get mock map data (GeoJSON format)"
  }
}
```

### GET /ping

Health check endpoint to verify the server is running.

**Example:**
```bash
curl http://localhost:5000/ping
```

**Response:**
```json
{
  "status": "ok",
  "message": "MCP Demo Map Server is running"
}
```

### GET /map

Returns mock geographic data in GeoJSON format.

**Example:**
```bash
curl http://localhost:5000/map
```

**Response:**
```json
{
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
    }
  ]
}
```

## Running Tests

Run the test suite with pytest:

```bash
pytest
```

For verbose output:
```bash
pytest -v
```

For coverage report:
```bash
pytest --cov=app --cov-report=html
```

## Project Structure

```
Mcpdemo/
├── app.py              # Main Flask application
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Code Quality

The code follows these principles:
- **Modular Design** - Separate functions for different concerns
- **Type Hints** - Python type annotations for clarity
- **Docstrings** - Comprehensive documentation for all functions
- **Testing** - Unit tests with mock data
- **PEP 8** - Python style guide compliance

## Development

To modify the mock data, edit the `get_mock_map_data()` function in `app.py`. The data follows the GeoJSON specification for geographic features.

## License

This is a demo project for educational purposes.

## MCP Concepts Demonstrated

This demo illustrates key MCP concepts:
- **Server Endpoints** - Clearly defined API routes
- **Data Format** - Structured JSON responses (GeoJSON)
- **Health Checks** - `/ping` endpoint for monitoring
- **Mock Data** - Demonstration without external dependencies
- **Modularity** - Separation of concerns in code structure