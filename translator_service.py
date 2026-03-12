import json
from litellm import completion
from config import GROQ_API_KEY, MODEL_NAME, SYSTEM_PROMPT

def get_segmented_translations(full_text):
    """Sends text to the AI and returns the structured JSON response."""
    formatted_prompt = SYSTEM_PROMPT.format(text=full_text)
    try:
        response = completion(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": formatted_prompt}],
            api_key=GROQ_API_KEY,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}