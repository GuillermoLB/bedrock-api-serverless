from app.core.config import Settings
from app.schemas.agent_schemas import AgentQuery
from sqlalchemy.orm import Session
from app.domain.schemas.text_generation_schemas import AgentResponse
from app.ml.text_generation.text_generation_pipeline import get_text_generation_pipeline
from app.repos import model_repo, text_generation_repo
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def process_agent_response(response: Dict[str, Any]) -> AgentResponse:
    """
    Process the agent response and return the response object.
    """
    agent_response = ""
    # Get the event stream
    event_stream = response.get('completion', response)
    for event in event_stream:
        if 'chunk' in event:
            chunk_text = event['chunk']['bytes'].decode('utf-8')
            # TODO: Add more data to the response object if needed
            agent_response.agent_response += chunk_text
    return AgentResponse(agent_response=agent_response)


def generate_response(
    bedrock: any,
    agent_query: AgentQuery,
    ) -> AgentResponse:
    """
    Generate text using AWS Bedrock agent based on the provided query.
    """
    logger.debug(f"Query: {agent_query.query}")
    
    # Invoke the Bedrock agent
    invoke_agent_response = bedrock.invoke_agent(
        agentId=agent_query.agent_id,
        agentAliasId=agent_query.agent_alias_id,
        inputText=agent_query.query,
        enableTrace=True # TODO: Check if with false response processing is easier
    )
    return process_agent_response(invoke_agent_response)
    
