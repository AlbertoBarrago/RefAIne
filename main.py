import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from anthropic import Anthropic
from anthropic.types import MessageParam
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="refAIne",
    description="Transform casual prompts into expert-level AI engineering prompts",
    version="1.0.0"
)

# Initialize LLM client based on provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()

if LLM_PROVIDER == "anthropic":
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        raise ValueError("ANTHROPIC_API_KEY required when LLM_PROVIDER=anthropic")

    client = Anthropic(api_key=anthropic_api_key)
    DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

elif LLM_PROVIDER == "openai":
    from openai import OpenAI

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        raise ValueError("OPENAI_API_KEY required when LLM_PROVIDER=openai")

    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_base_url
    )
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

else:
    logger.error(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")
    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}. Use 'anthropic' or 'openai'")

logger.info(f"Initialized {LLM_PROVIDER} provider with model {DEFAULT_MODEL}")

# Request/Response models
class RefineRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The casual user prompt to refine")

class RefineResponse(BaseModel):
    original: str
    refined: str
    model: str

# System prompt for refinement
REFINEMENT_SYSTEM_PROMPT = """You are an expert prompt engineer specializing in software development tasks.

Your role is to transform casual, ambiguous user prompts into clear, comprehensive, expert-level prompts that will produce better AI-generated code and solutions.

When refining prompts, you should:

1. **Add Context**: Assume software development context and specify relevant details
2. **Add Specificity**: Include programming language, framework, libraries, and versions when relevant
3. **Define Requirements**: Make implicit requirements explicit (error handling, validation, edge cases)
4. **Include Best Practices**: Add expectations for code quality, testing, documentation, security
5. **Clarify Constraints**: Specify performance considerations, compatibility, or architectural patterns
6. **Maintain Intent**: Keep the core request intact while enhancing clarity
7. **Be Concise**: Comprehensive but not verbose - stay focused and actionable

Output ONLY the refined prompt. Do not include explanations, meta-commentary, or preamble."""


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "refAIne",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.post("/refine", response_model=RefineResponse)
async def refine_prompt(request: RefineRequest):
    """
    Refine a casual prompt into an expert-level AI engineering prompt.

    Takes a user's casual prompt and transforms it using Claude to add
    specificity, best practices, and software engineering context.
    """
    global refined_prompt
    try:
        logger.info(f"Refining prompt: {request.prompt[:100]}...")

        # Call LLM API based on provider
        if LLM_PROVIDER == "anthropic":
            messages: list[MessageParam] = [
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
            message = client.messages.create(
                model=DEFAULT_MODEL,
                max_tokens=2000,
                system=REFINEMENT_SYSTEM_PROMPT,
                messages=messages
            )
            refined_prompt = message.content[0].text.strip()

        elif LLM_PROVIDER == "openai":
            from openai.types.chat import ChatCompletionMessageParam

            openai_messages: list[ChatCompletionMessageParam] = [
                {
                    "role": "system",
                    "content": REFINEMENT_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ]
            response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                max_tokens=2000,
                messages=openai_messages
            )
            refined_prompt = response.choices[0].message.content.strip()

        logger.info("Successfully refined prompt")

        return RefineResponse(
            original=request.prompt,
            refined=refined_prompt,
            model=DEFAULT_MODEL
        )

    except Exception as e:
        logger.error(f"Error refining prompt with {LLM_PROVIDER} provider: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refine prompt using {LLM_PROVIDER}: {str(e)}"
        )
