from typing import Any
import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_create_session(client: AsyncClient, bedrock: Any):
    """Test creating a new session via the API endpoint"""
    
    # Make request to create session endpoint
    response = await client.post("/api/copilot/sessions/")
    
    # Check response status code
    assert response.status_code == 200
    
    # Parse response data
    session_data = response.json()
    
    # Validate response structure
    assert "session_id" in session_data
    assert isinstance(session_data["session_id"], str)
    assert len(session_data["session_id"]) > 0
