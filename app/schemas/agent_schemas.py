from typing import Optional
from pydantic import BaseModel, field_validator

from app.error.codes import Errors
from app.error.exceptions import ModelException, TextGenerationException

class AgentResponseBase(BaseModel):
    agent_id: str = None
    agent_alias_id: str = None


class AgentResponseCreate(AgentResponseBase):
    agent_query: str

    @field_validator("prompt")
    def query_must_not_be_empty(cls, value): # Validation placeholder
        if not value.strip():
            raise TextGenerationException(error=Errors.E004, code=400)
        return value


class AgentResponseRead(BaseModel): # We don't need to return the ids
    agent_response: str

    # TODO: @serializer for formatting the agent response for the route response