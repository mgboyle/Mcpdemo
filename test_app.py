"""
Unit tests for MCP Demo Map Server

Tests all API endpoints using mock responses and Flask's test client.
"""

import pytest
from app import app, get_mock_map_data


@pytest.fixture
def client():
    """
    Create a test client for the Flask application.
    
    Yields:
        FlaskClient: A test client for making requests to the app.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ping_endpoint(client):
    """
    Test the /ping health check endpoint.
    
    Verifies:
    - Response status code is 200
    - Response contains correct status and message
    """
    response = client.get('/ping')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'MCP Demo Map Server is running'


def test_map_endpoint(client):
    """
    Test the /map endpoint that returns mock geographic data.
    
    Verifies:
    - Response status code is 200
    - Response is in GeoJSON format
    - Contains expected feature collection structure
    - Features have required geometry and properties
    """
    response = client.get('/map')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['type'] == 'FeatureCollection'
    assert 'features' in data
    assert len(data['features']) > 0
    
    # Verify structure of first feature
    first_feature = data['features'][0]
    assert first_feature['type'] == 'Feature'
    assert 'geometry' in first_feature
    assert 'properties' in first_feature
    assert 'coordinates' in first_feature['geometry']
    assert 'name' in first_feature['properties']


def test_root_endpoint(client):
    """
    Test the root / endpoint that provides API information.
    
    Verifies:
    - Response status code is 200
    - Response contains API metadata
    - Endpoints information is present
    """
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['name'] == 'MCP Demo Map Server'
    assert 'version' in data
    assert 'description' in data
    assert 'endpoints' in data
    
    # Verify all expected endpoints are documented
    endpoints = data['endpoints']
    assert '/' in endpoints
    assert '/ping' in endpoints
    assert '/map' in endpoints


def test_get_mock_map_data():
    """
    Test the get_mock_map_data() function directly.
    
    Verifies:
    - Returns a dictionary with correct structure
    - Contains feature collection with multiple features
    - Each feature has valid geographic coordinates
    """
    data = get_mock_map_data()
    
    assert isinstance(data, dict)
    assert data['type'] == 'FeatureCollection'
    assert isinstance(data['features'], list)
    assert len(data['features']) == 3
    
    # Verify each feature has valid structure
    for feature in data['features']:
        assert feature['type'] == 'Feature'
        assert 'geometry' in feature
        assert 'properties' in feature
        
        geometry = feature['geometry']
        assert geometry['type'] == 'Point'
        assert len(geometry['coordinates']) == 2
        
        properties = feature['properties']
        assert 'name' in properties
        assert 'population' in properties
        assert 'country' in properties


def test_map_data_consistency(client):
    """
    Test that multiple requests to /map return consistent data.
    
    Verifies:
    - Data structure remains consistent across requests
    - Same number of features returned
    """
    response1 = client.get('/map')
    response2 = client.get('/map')
    
    data1 = response1.get_json()
    data2 = response2.get_json()
    
    assert len(data1['features']) == len(data2['features'])
    assert data1['type'] == data2['type']


def test_invalid_endpoint(client):
    """
    Test that invalid endpoints return 404.
    
    Verifies:
    - Non-existent routes return 404 status
    """
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_ping_method_not_allowed(client):
    """
    Test that non-GET methods on /ping are not allowed.
    
    Verifies:
    - POST request returns 405 Method Not Allowed
    """
    response = client.post('/ping')
    assert response.status_code == 405


def test_map_method_not_allowed(client):
    """
    Test that non-GET methods on /map are not allowed.
    
    Verifies:
    - POST request returns 405 Method Not Allowed
    """
    response = client.post('/map')
    assert response.status_code == 405


def test_response_content_type(client):
    """
    Test that responses have correct Content-Type header.
    
    Verifies:
    - All endpoints return JSON content type
    """
    endpoints = ['/', '/ping', '/map']
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert 'application/json' in response.content_type
