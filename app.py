import streamlit as st
from litellm import completion
import json
import os
import streamlit.components.v1 as components
import time

# --- APP CONFIGURATION ---
api_key = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """
You are a translation editor specializing in Brazilian Portuguese to English. 
Your task is to:
1. Divide the provided text into logical, readable segments (sentences or short meaningful phrases).
2. For EACH segment, provide 3 distinct and high-quality English translations.

Return ONLY a JSON object with this exact structure:
{{
  "segments": [
    {{
      "original": "Texto original em português",
      "v1": "First English variation",
      "v2": "Second English variation",
      "v3": "Third English variation"
    }},
    ...
  ]
}}

Text to process (PT-BR): {text}
"""

def get_segmented_translations(full_text):
    formatted_prompt = SYSTEM_PROMPT.format(text=full_text)
    try:
        response = completion(
            model="groq/openai/gpt-oss-120b",
            messages=[{"role": "user", "content": formatted_prompt}],
            api_key=api_key,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# --- CALLBACK ---
def handle_translation():
    if st.session_state.source_text_key.strip():
        st.session_state.text_to_process = st.session_state.source_text_key
        st.session_state.source_text_key = ""
        st.session_state.translation_data = None
        # Increment the 'run_id' to force all checkbox keys to change
        st.session_state.run_id += 1 
    else:
        st.session_state.text_to_process = None

# --- UI SETUP ---
st.set_page_config(page_title="Translator", layout="centered")

# Initialize essential states
if "translation_data" not in st.session_state:
    st.session_state.translation_data = None
if "text_to_process" not in st.session_state:
    st.session_state.text_to_process = None
if "run_id" not in st.session_state:
    st.session_state.run_id = 0

st.title("Portuguese → English")

source_text = st.text_area(
    "Source:", 
    placeholder="Digite e aperte Ctrl+Enter...", 
    height=150, 
    label_visibility="collapsed",
    key="source_text_key" 
)

if st.button("Translate (Ctrl+Enter)", use_container_width=True, on_click=handle_translation, key="translate_btn"):
    if st.session_state.text_to_process:
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(st.session_state.text_to_process)

# --- DISPLAY & SELECTION ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    selected_versions = []

    # Current run_id makes these keys unique to this specific translation batch
    rid = st.session_state.run_id

    for i, item in enumerate(st.session_state.translation_data["segments"]):
        # The key now includes the run_id, forcing a reset every time rid changes
        v1_check = st.checkbox(item['v1'], key=f"run_{rid}_seg_{i}_v1")
        if v1_check: selected_versions.append(item['v1'])
            
        v2_check = st.checkbox(item['v2'], key=f"run_{rid}_seg_{i}_v2")
        if v2_check: selected_versions.append(item['v2'])
            
        v3_check = st.checkbox(item['v3'], key=f"run_{rid}_seg_{i}_v3")
        if v3_check: selected_versions.append(item['v3'])
        
        st.write("") 

    if selected_versions:
        st.divider()
        st.code(" ".join(selected_versions), language=None)

# --- KEYBOARD SHORTCUT ---
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.keyCode === 13) {
        const buttons = doc.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.innerText.includes("Translate (Ctrl+Enter)")) {
                btn.click();
                break;
            }
        }
    }
});
</script>
""", height=0, width=0)