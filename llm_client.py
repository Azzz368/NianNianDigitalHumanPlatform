import json
import os
import time
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")
FALLBACK_MODELS = [
    item.strip()
    for item in os.getenv("OPENAI_FALLBACK_MODELS", "").split(",")
    if item.strip()
]


def _build_client() -> OpenAI:
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


CLIENT = _build_client()


def call_skill(skill_name: str, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Call LLM with JSON mode and return parsed dict or error structure."""
    last_error: Optional[str] = None
    for model_name in [MODEL_NAME, *FALLBACK_MODELS]:
        for attempt in range(1, 4):
            try:
                response = CLIENT.chat.completions.create(
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
