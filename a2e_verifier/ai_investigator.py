import os

from groq import Groq


def ai_investigate(
    authorized: dict,
    executed: dict,
    verification: dict,
    investigation: dict,
) -> str | None:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are a cybersecurity analyst investigating an AI-agent authorization
integrity violation.

The deterministic security verifier has already made the security decision.
Do NOT override or change that decision.

Authorized action:
{authorized}

Executed action:
{executed}

Deterministic verification result:
{verification}

Existing investigation:
{investigation}

Provide a concise security analysis containing:
1. What changed between authorization and execution.
2. Why the change matters from a security perspective.
3. The most likely point in the action flow where the drift occurred.
4. Two concrete investigation/remediation steps.

Do not invent facts that are not present in the supplied data.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise cybersecurity analyst.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception:
        return None
