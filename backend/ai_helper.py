import os
import time
import logging
from typing import Optional

# --- OpenAI client (modern SDK) ---
try:
    from openai import OpenAI  # modern v1+ SDK
    # Exception classes may differ by version; fall back to Exception if import fails.
    try:
        from openai import APIError, RateLimitError, APITimeoutError, APIConnectionError
    except Exception:  # pragma: no cover
        APIError = RateLimitError = APITimeoutError = APIConnectionError = Exception
except Exception as e:  # pragma: no cover
    OpenAI = None
    APIError = RateLimitError = APITimeoutError = APIConnectionError = Exception
    logging.warning("OpenAI SDK not available: %s", e)

# --- Config ---
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # cost-effective default
MIN_INTERVAL = float(os.getenv("OPENAI_MIN_INTERVAL", "1.5"))  # seconds between calls
TIMEOUT_SECS = int(os.getenv("OPENAI_TIMEOUT", "30"))

_client: Optional[OpenAI] = None
if API_KEY and OpenAI is not None:
    _client = OpenAI(api_key=API_KEY)
else:
    logging.warning(
        "AI features disabled: OPENAI_API_KEY missing or OpenAI SDK not installed."
    )

_last_request_ts = 0.0


def _throttle() -> None:
    """Simple rate limiter to avoid hammering the API on free tiers."""
    global _last_request_ts
    now = time.time()
    wait = MIN_INTERVAL - (now - _last_request_ts)
    if wait > 0:
        time.sleep(wait)
    _last_request_ts = time.time()


def _fallback(topic: str) -> str:
    """Safe, no-crash fallback message when AI is unavailable."""
    return (
        f"[AI temporarily unavailable]\n"
        f"Quick guide to '{topic}':\n"
        f"• Break it into 3 basics you must know.\n"
        f"• Learn by doing: try one 10–15 min practice task.\n"
        f"• Ask a peer/mentor to review your result and give 1 improvement tip."
    )


def explain_topic(topic: str) -> str:
    """
    Explain a topic simply for a beginner, with friendly tone and 3 practical steps.
    Never raises if API is unavailable—returns a helpful fallback instead.
    """
    if not _client:
        return _fallback(topic)

    _throttle()

    system = (
        "You are a practical vocational coach for African learners. "
        "Explain clearly, keep it friendly, and end with 3 quick practice steps."
    )
    user = (
        f"Explain '{topic}' simply for a beginner hustler. "
        "Use short bullets and real-world examples relevant to Nigeria when possible."
    )

    try:
        resp = _client.chat.completions.create(
            model=MODEL,  # e.g., gpt-4o or gpt-4o-mini
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.5,
            max_tokens=350,
            timeout=TIMEOUT_SECS,  # supported in recent SDKs
        )
        return (resp.choices[0].message.content or "").strip()

    except RateLimitError:
        # brief backoff and one retry
        time.sleep(2.0)
        try:
            resp = _client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.5,
                max_tokens=350,
                timeout=TIMEOUT_SECS,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            logging.exception("OpenAI rate limit after retry: %s", e)
            return _fallback(topic)

    except (APITimeoutError, APIConnectionError, APIError) as e:
        logging.exception("OpenAI API error: %s", e)
        return _fallback(topic)

    except Exception as e:  # catch-all so the API never crashes your app
        logging.exception("Unexpected AI error: %s", e)
        return _fallback(topic)

