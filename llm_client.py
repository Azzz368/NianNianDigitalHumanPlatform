import json
import os
import time
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PRIMARY_MODEL = os.getenv("OPENAI_MODEL", "qwen3.5:9b")
FALLBACK_MODELS = [
    item.strip()
    for item in os.getenv("OPENAI_FALLBACK_MODELS", "").split(",")
    if item.strip()
]


def _build_client(base_url: Optional[str], api_key: Optional[str]) -> OpenAI:
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


PRIMARY_CLIENT = _build_client(
    os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    os.getenv("OPENAI_API_KEY", "lm-studio"),
)
FALLBACK_CLIENT = _build_client(
    os.getenv("OPENAI_FALLBACK_BASE_URL"),
    os.getenv("OPENAI_FALLBACK_API_KEY", os.getenv("OPENAI_API_KEY", "")),
)


def _iter_model_clients():
    model_queue = [(PRIMARY_MODEL, PRIMARY_CLIENT)]
    for fallback_model in FALLBACK_MODELS:
        model_queue.append((fallback_model, FALLBACK_CLIENT or PRIMARY_CLIENT))
    return model_queue


def call_skill(skill_name: str, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call LLM with JSON mode and return parsed dict or error structure."""
    last_error: Optional[str] = None
    for model_name, client in _iter_model_clients():
        for attempt in range(1, 4):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": json.dumps(user_payload, ensure_ascii=False),
                        },
                    ],
                    temperature=0.4,
                )
                content = response.choices[0].message.content or "{}"
                return json.loads(content)
            except Exception as exc:  # pragma: no cover - runtime API errors
                last_error = f"{model_name}: {exc}"
                if attempt < 3:
                    time.sleep(2)

    return {"error": True, "skill": skill_name, "message": last_error or "Unknown error"}


def call_freeform(system_prompt: str, user_content: str) -> str:
    last_error: Optional[str] = None
    for model_name, client in _iter_model_clients():
        for attempt in range(1, 4):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.4,
                )
                return response.choices[0].message.content or ""
            except Exception as exc:  # pragma: no cover - runtime API errors
                last_error = f"{model_name}: {exc}"
                if attempt < 3:
                    time.sleep(2)

    return f"[ERROR] {last_error or 'Unknown error'}"


def call_structured(system_prompt: str, user_content: str) -> Dict[str, Any]:
    last_error: Optional[str] = None
    for model_name, client in _iter_model_clients():
        for attempt in range(1, 4):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.2,
                )
                content = response.choices[0].message.content or "{}"
                return json.loads(content)
            except Exception as exc:  # pragma: no cover - runtime API errors
                last_error = f"{model_name}: {exc}"
                if attempt < 3:
                    time.sleep(2)

    return {"error": True, "message": last_error or "Unknown error"}
