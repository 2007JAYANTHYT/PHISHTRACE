import pytest
from app.services.gemma_provider import (
    AVAILABLE_LLM_MODELS,
    compare_models_for_email,
    execute_prompt_playground
)
from app.services.ai_copilot import run_copilot_assistant
from app.db.seed import seed_database_and_samples
from app.db.database import db

def test_available_llm_models_catalog():
    """Verify catalog returns all 5 open-weight models with metadata."""
    assert len(AVAILABLE_LLM_MODELS) == 5
    model_ids = [m["id"] for m in AVAILABLE_LLM_MODELS]
    assert "google/gemma-2-9b-it" in model_ids
    assert "meta/llama-3.2-11b-vision-instruct" in model_ids
    assert "mistralai/Mistral-7B-Instruct-v0.3" in model_ids
    assert "qwen/qwen-2.5-7b-instruct" in model_ids
    assert "phishtrace/cyber-forensics-nlp" in model_ids
    for m in AVAILABLE_LLM_MODELS:
        assert m["open_source"] is True
        assert len(m["context_window"]) > 0

def test_multimodel_consensus_comparison():
    """Verify multi-model consensus evaluates all 5 models."""
    seed_database_and_samples()
    emails = db.get_all_email_details()
    assert len(emails) > 0
    target_email = emails[0]

    data = compare_models_for_email(target_email)
    assert data["message_id"] == target_email.id
    assert "consensus_verdict" in data
    assert "agreement_percentage" in data
    assert len(data["evaluations"]) == 5

    for ev in data["evaluations"]:
        assert "threat_verdict" in ev
        assert "risk_score" in ev
        assert "confidence" in ev
        assert "reasoning" in ev
        assert "latency_ms" in ev

def test_prompt_playground_execution():
    """Verify interactive prompt playground generates responses for queries."""
    seed_database_and_samples()
    emails = db.get_all_email_details()
    target_email = emails[0]

    # 1. KQL query generation
    res_kql = execute_prompt_playground(
        "meta/llama-3.2-11b-vision-instruct",
        "Synthesize a Sentinel KQL query for hunting this email",
        target_email
    )
    assert "EmailEvents" in res_kql["response_text"]
    assert res_kql["latency_ms"] > 0

    # 2. YARA rule generation
    res_yara = execute_prompt_playground(
        "qwen/qwen-2.5-7b-instruct",
        "Generate a YARA rule for this threat",
        target_email
    )
    assert "rule Custom_Detect" in res_yara["response_text"]

def test_ai_copilot_soc_rule_synthesis():
    """Verify interactive SOC co-pilot assistant synthesizes detection rules."""
    seed_database_and_samples()
    emails = db.get_all_email_details()
    target_email = emails[0]

    copilot_res = run_copilot_assistant(
        "Write a YARA rule and Microsoft Sentinel hunting query for this incident",
        target_email
    )
    assert copilot_res.yara_rule is not None
    assert "rule PhishTrace_" in copilot_res.yara_rule
    assert copilot_res.kql_query is not None
    assert "EmailEvents" in copilot_res.kql_query
    assert len(copilot_res.suggested_actions) > 0
