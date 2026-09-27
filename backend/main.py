import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

from prompt_builder import build_prompt, build_transform_prompt


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is not configured. "
        "Please check your backend/.env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Verbo API",
    description="Backend for Verbo - an AI Text Generation Studio",
    version="0.1.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST / RESPONSE MODELS
# ============================================================

class GenerateRequest(BaseModel):
    topic: str
    mode: str
    length: str
    tone: str
    audience: str
    complexity: str = "Intermediate"
    custom_instructions: str = ""


class GenerateResponse(BaseModel):
    content: str


class TransformRequest(BaseModel):
    text: str
    transform_type: str
    target_tone: str = ""


class TransformResponse(BaseModel):
    result: str


# ============================================================
# FRIENDLY ERROR HANDLER
# ============================================================

def friendly_error(exc: Exception) -> str:
    """
    Convert technical Gemini/API errors into messages
    that are safe and understandable for normal users.
    """

    text = str(exc).lower()

    if (
        "503" in text
        or "unavailable" in text
        or "overloaded" in text
    ):
        return (
            "The AI model is currently busy handling high demand. "
            "Please try again in a moment."
        )

    if (
        "429" in text
        or "quota" in text
        or "rate" in text
        or "resource_exhausted" in text
    ):
        return (
            "You've hit the request limit for now. "
            "Please wait a moment and try again."
        )

    if (
        "api key" in text
        or "401" in text
        or "permission" in text
        or "unauthorized" in text
        or "unauthenticated" in text
    ):
        return (
            "There's an issue with the server's API key configuration. "
            "Please contact the administrator."
        )

    if (
        "404" in text
        and "model" in text
    ):
        return (
            "The selected AI model is currently unavailable. "
            "Please try again later."
        )

    if (
        "timeout" in text
        or "timed out" in text
    ):
        return (
            "The request took too long and timed out. "
            "Please try again."
        )

    if (
        "connection" in text
        or "network" in text
        or "dns" in text
    ):
        return (
            "Could not reach the AI service. "
            "Please check your internet connection."
        )

    if (
        "safety" in text
        or "blocked" in text
    ):
        return (
            "The generated content was blocked by safety filters. "
            "Try rephrasing your topic."
        )

    return (
        "Something went wrong while generating your content. "
        "Please try again."
    )


# ============================================================
# GEMINI CALL
# ============================================================

def call_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text


# ============================================================
# GEMINI CALL WITH RETRY
# ============================================================

def call_gemini_with_retry(
    prompt: str,
    retries: int = 2,
    delay: float = 1.5,
) -> str:
    """
    Retry temporary 503/unavailable errors.
    Other errors are raised immediately.
    """

    last_exception = None

    for attempt in range(retries + 1):

        try:
            return call_gemini(prompt)

        except Exception as exc:

            last_exception = exc

            error_text = str(exc).lower()

            is_busy = (
                "503" in error_text
                or "unavailable" in error_text
                or "overloaded" in error_text
            )

            if not is_busy:
                raise

            if attempt < retries:
                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying... ({attempt + 1}/{retries})"
                )

                time.sleep(delay)

    raise last_exception


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "verbo-backend",
    }


# ============================================================
# GENERATE
# ============================================================

@app.post("/generate", response_model=GenerateResponse)
def generate_content(request: GenerateRequest):

    # Empty topic
    if not request.topic.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a topic before generating.",
        )

    # Input too long
    if len(request.topic) > 6000:
        raise HTTPException(
            status_code=400,
            detail=(
                "Your input is too long. "
                "Please shorten it and try again."
            ),
        )

    # Build prompt
    prompt = build_prompt(
        topic=request.topic,
        mode=request.mode,
        length=request.length,
        tone=request.tone,
        audience=request.audience,
        complexity=request.complexity,
        custom_instructions=request.custom_instructions,
    )

    print("")
    print("=" * 60)
    print("GENERATING CONTENT")
    print("=" * 60)
    print(f"Model: {GEMINI_MODEL}")
    print(f"Topic: {request.topic}")
    print(f"Mode: {request.mode}")
    print(f"Length: {request.length}")
    print(f"Tone: {request.tone}")
    print(f"Audience: {request.audience}")
    print(f"Complexity: {request.complexity}")
    print("=" * 60)

    try:

        content = call_gemini_with_retry(prompt)

        if not content or not content.strip():
            raise HTTPException(
                status_code=502,
                detail=(
                    "The AI returned an empty response. "
                    "Please try again."
                ),
            )

        print("Generation successful.")

        return GenerateResponse(
            content=content
        )

    except HTTPException:
        raise

    except Exception as exc:

        print("")
        print("Gemini error:")
        print(str(exc))

        raise HTTPException(
            status_code=502,
            detail=friendly_error(exc),
        )


# ============================================================
# TRANSFORM
# ============================================================

@app.post("/transform", response_model=TransformResponse)
def transform_text(request: TransformRequest):

    # Empty text
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please paste some text before transforming it.",
        )

    # Text too long
    if len(request.text) > 12000:
        raise HTTPException(
            status_code=400,
            detail=(
                "The text is too long. "
                "Please shorten it and try again."
            ),
        )

    # Build transformation prompt
    prompt = build_transform_prompt(
        text=request.text,
        transform_type=request.transform_type,
        target_tone=request.target_tone,
    )

    print("")
    print("=" * 60)
    print("TRANSFORMING CONTENT")
    print("=" * 60)
    print(f"Model: {GEMINI_MODEL}")
    print(f"Transform: {request.transform_type}")
    print("=" * 60)

    try:

        result = call_gemini_with_retry(prompt)

        if not result or not result.strip():
            raise HTTPException(
                status_code=502,
                detail=(
                    "The AI returned an empty response. "
                    "Please try again."
                ),
            )

        print("Transformation successful.")

        return TransformResponse(
            result=result
        )

    except HTTPException:
        raise

    except Exception as exc:

        print("")
        print("Gemini error:")
        print(str(exc))

        raise HTTPException(
            status_code=502,
            detail=friendly_error(exc),
        )

