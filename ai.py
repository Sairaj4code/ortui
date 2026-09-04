import os
import requests


def ask_ai(messages_list):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/free",  # Make sure this matches an active free model slug on OpenRouter if needed
                "messages": messages_list,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        # Extract just the assistant's reply text safely
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error connecting to AI: {e}"
