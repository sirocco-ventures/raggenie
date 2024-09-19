from pydantic import BaseModel, Field
class SystemPrompt(BaseModel):
    template: str = Field(
        ...,
        description="The template used for system-level prompt generation."
    )

class UserPrompt(BaseModel):
    template: str = Field(
        ...,
        description="The template used for user-level prompt generation."
    )

class RegenerationPrompt(BaseModel):
    template: str = Field(
        ...,
        description="The template used for regenerating the response prompt."
    )

class Prompt(BaseModel):
    base_prompt: str = Field(
        ...,
        description="The base prompt structure combining system and user prompts."
    )
    system_prompt: SystemPrompt = Field(
        ...,
        description="The system prompt details."
    )
    user_prompt: UserPrompt = Field(
        ...,
        description="The user prompt details."
    )
    regeneration_prompt: RegenerationPrompt = Field(
        ...,
        description="The regeneration prompt details."
    )