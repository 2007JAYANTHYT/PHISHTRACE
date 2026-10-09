from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ...models.schemas import (
    AiStatus, AiCopilotRequest, AiCopilotResponse,
    LlmModelInfo, LlmComparisonResult,
    PromptPlaygroundRequest, PromptPlaygroundResponse
)
from ...services.gemma_provider import (
    gemma_service, AVAILABLE_LLM_MODELS,
    compare_models_for_email, execute_prompt_playground
)
from ...services.ai_copilot import run_copilot_assistant
from ...db.database import db

router = APIRouter()

class AiConfigUpdate(BaseModel):
    model_config = {"protected_namespaces": ()}
    groq_api_key: Optional[str] = None
    nvidia_api_key: Optional[str] = None
    model_name: Optional[str] = None

class ModelComparisonRequest(BaseModel):
    message_id: str

@router.get("/ai/status", response_model=AiStatus)
def get_ai_status():
    stat = gemma_service.get_status()
    return AiStatus(
        available=stat["available"],
        provider=stat["provider"],
        model=stat["model"],
        mode=stat["mode"],
        latency_ms=12.4 if stat["mode"] == "Built-in Zero-Latency Engine" else 350.0,
        message=stat["message"]
    )

@router.get("/ai/models", response_model=List[LlmModelInfo])
def get_available_llm_models():
    """Returns the catalog of available Open-Source and Open-Weights LLMs."""
    return [LlmModelInfo(**m) for m in AVAILABLE_LLM_MODELS]

@router.post("/ai/config")
def update_ai_config(cfg: AiConfigUpdate):
    """Dynamically updates Open-Source AI provider settings from UI."""
    if cfg.groq_api_key is not None:
        gemma_service.groq_key = cfg.groq_api_key.strip()
    if cfg.nvidia_api_key is not None:
        gemma_service.nvidia_key = cfg.nvidia_api_key.strip()
    if cfg.model_name is not None and cfg.model_name.strip():
        gemma_service.model_name = cfg.model_name.strip()
    
    return {
        "status": "updated",
        "active_status": gemma_service.get_status()
    }

@router.post("/ai/copilot", response_model=AiCopilotResponse)
def invoke_ai_copilot(req: AiCopilotRequest):
    """
    Interactive Open-Source AI Security Co-Pilot endpoint.
    Answers analyst questions, synthesizes YARA rules, M365 rules, KQL, Splunk, and Sigma rules.
    """
    email = db.get_email(req.message_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email record not found for AI Co-Pilot reasoning.")

    return run_copilot_assistant(req.user_prompt, email)

@router.post("/ai/compare", response_model=LlmComparisonResult)
def compare_llm_models(req: ModelComparisonRequest):
    """
    Executes multi-model consensus comparison:
    Runs Google Gemma 2, Meta Llama 3.3, Mistral 7B, Qwen 2.5, and Cyber Engine on the email.
    """
    email = db.get_email(req.message_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found for multi-model comparison.")

    res = compare_models_for_email(email)
    return LlmComparisonResult(**res)

@router.post("/ai/playground", response_model=PromptPlaygroundResponse)
def run_prompt_playground(req: PromptPlaygroundRequest):
    """
    Interactive Prompt Playground allowing arbitrary prompt execution
    against any selected LLM model.
    """
    email = db.get_email(req.message_id) if req.message_id else None
    res = execute_prompt_playground(req.model_id, req.user_prompt, email)
    return PromptPlaygroundResponse(**res)
