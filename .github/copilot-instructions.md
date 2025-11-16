# Copilot Instructions for MCP Demo Map Server

## Project Overview
This is a lightweight Flask demo server illustrating Model Context Protocol (MCP) concepts through a simple GeoJSON map API. The codebase prioritizes clarity and educational value over production complexity.

## Architecture & Key Patterns

**Single-File Flask Application**: All server logic lives in `app.py` with clear separation of concerns:
- `get_mock_map_data()` - Data generation (returns GeoJSON FeatureCollection)
- Route handlers (`/`, `/ping`, `/map`) - Each returns tuple of `(jsonify(dict), status_code)`
- All endpoints are GET-only; POST/PUT/DELETE return 405

**GeoJSON Format**: The `/map` endpoint returns standard GeoJSON FeatureCollections with Point geometries. Features include `geometry.coordinates` (lon, lat) and `properties` (name, population, country).

**Type Annotations**: All functions use Python type hints (e.g., `Dict[str, Any]`, `tuple[Dict[str, str], int]`). Maintain this pattern when adding functions.

## Development Workflow

**Running Locally**:
```bash
# Setup (first time)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start server (debug mode enabled by default)
python app.py  # Runs on http://localhost:5000

# Disable debug mode
FLASK_DEBUG=false python app.py
```

**Testing**:
```bash
pytest              # Run all tests
pytest -v           # Verbose output
pytest --cov=app    # With coverage
```

**Test Structure**: All tests use the `client` fixture from `test_app.py`. Pattern:
```python
def test_endpoint_name(client):
    response = client.get('/endpoint')
    assert response.status_code == 200
    data = response.get_json()
    # Assert on data structure
```

## Project-Specific Conventions

1. **Endpoint Documentation**: Every route handler has a docstring explaining its purpose and return format
2. **Mock Data Location**: All geographic data is hardcoded in `get_mock_map_data()` - no external files or databases
3. **Response Format**: Always `return jsonify({...}), status_code` (never bare dicts)
4. **Test Coverage**: New endpoints require tests for:
   - Happy path (200 response)
   - Method not allowed (405 for non-GET)
   - Response structure validation
   - Content-Type header (`application/json`)
5. **Dependencies**: Minimal by design - only Flask, pytest, pytest-cov in `requirements.txt`

## Adding New Features

**New Endpoint Example**:
```python
@app.route('/cities/<country>', methods=['GET'])
def cities_by_country(country: str) -> tuple[Dict[str, Any], int]:
    """Filter cities by country."""
    all_data = get_mock_map_data()
    filtered = [f for f in all_data['features'] if f['properties']['country'] == country]
    return jsonify({"type": "FeatureCollection", "features": filtered}), 200
```

Then add corresponding tests in `test_app.py` using the `client` fixture.

**Modifying Mock Data**: Edit the hardcoded list in `get_mock_map_data()`. Coordinates are `[longitude, latitude]` (GeoJSON standard).

## Critical Notes

- **Debug Mode**: `app.run(debug=True)` is intentional for demos - README warns about production use
- **No Authentication**: This is a demo server; all endpoints are public
- **Port 5000**: Flask default; bound to `0.0.0.0` for container compatibility
- **No Database**: All data is in-memory mock data regenerated per request
