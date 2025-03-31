import logging
from app.schemas.agent_schemas import AgentQuery
from app.schemas.text_generation_schemas import TextGenerationCreate
from app.services import agent_service
from fastapi import APIRouter
from app.dependencies import BedrockDep, SessionDep, SettingsDep, UserDep
from app.repos import user_repo
from app.schemas.user_schemas import UserRead, UserCreate


responses_router = APIRouter(
    tags=["responses"],
    prefix="/responses",
)

logger = logging.getLogger(__name__)


async def create_text_generation(
    agent_query: AgentQuery,
    bedrock: BedrockDep,
    settings: SettingsDep,
    session: SessionDep,
    current_user: UserDep,
):
    """
    Generate text using AI model based on provided prompt.

    Requires valid authentication token.

    Parameters:
    - **prompt**: The input text to generate from

    Returns:
    - **prompt**: Original input text 
    - **generated_text**: AI generated response
    """
    try:
        logger.info(f"Generating text for prompt: {
                    agent_query.agent_query}")
        

        
        agent_response = agent_service.generate_text(
            agent_id=agent_query.agent_id,
            agent_alias_id=agent_query.agent_alias_id,
            session_id=current_user.session_id,
            bedrock=bedrock,
            agent_query=agent_,
        )

        logger.info(f"Agent_response: {agent_response}")
        return text_generation

    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)