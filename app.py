import streamlit as st
from litellm import completion
import json
import os
import streamlit.components.v1 as components

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

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Translator Builder", layout="centered")

st.title("Portuguese → English Builder")

if "translation_data" not in st.session_state:
    st.session_state.translation_data = None

source_text = st.text_area("Source:", placeholder="Cole seu texto...", height=150, label_visibility="collapsed")

# We give the button a unique label/key so the JavaScript can find it
translate_clicked = st.button("Translate (Ctrl+Enter)", use_container_width=True, key="translate_btn")

if translate_clicked:
    if source_text.strip():
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(source_text)
    else:
        st.warning("Por favor, insira um texto.")

# --- DISPLAY & INDIVIDUAL CHECKBOXES ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    selected_versions = []

    for i, item in enumerate(st.session_state.translation_data["segments"]):
        v1_check = st.checkbox(item['v1'], key=f"seg_{i}_v1")
        if v1_check: selected_versions.append(item['v1'])
            
        v2_check = st.checkbox(item['v2'], key=f"seg_{i}_v2")
        if v2_check: selected_versions.append(item['v2'])
            
        v3_check = st.checkbox(item['v3'], key=f"seg_{i}_v3")
        if v3_check: selected_versions.append(item['v3'])
        
        st.write("") 

    if selected_versions:
        st.divider()
        st.subheader("Selected Text")
        final_string = " ".join(selected_versions)
        st.code(final_string, language=None)
        
        if st.button("Reset All Selections"):
            for key in st.session_state.keys():
                if key.startswith("seg_"):
                    st.session_state[key] = False
            st.rerun()

# --- KEYBOARD SHORTCUT (Ctrl + Enter) ---
components.html(
    """
<script>
const doc = window.parent.document;
doc.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.keyCode === 13) {
        // Find the button by its text content and click it
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
""",
    height=0,
    width=0,
)