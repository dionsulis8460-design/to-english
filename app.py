import streamlit as st
from translator_service import get_segmented_translations
from ui_components import inject_keyboard_shortcut, render_segment_options

# --- CALLBACKS ---
def handle_translation():
    """Wipes the input and resets state for a new translation run."""
    if st.session_state.source_text_key.strip():
        st.session_state.text_to_process = st.session_state.source_text_key
        st.session_state.source_text_key = ""
        st.session_state.translation_data = None
        st.session_state.run_id += 1 
    else:
        st.session_state.text_to_process = None

# --- APP INITIALIZATION ---
st.set_page_config(page_title="Translator", layout="centered")

if "translation_data" not in st.session_state:
    st.session_state.translation_data = None
if "text_to_process" not in st.session_state:
    st.session_state.text_to_process = None
if "run_id" not in st.session_state:
    st.session_state.run_id = 0

# --- USER INPUT ---
st.text_area(
    "Source:", 
    placeholder="...", 
    height=150, 
    label_visibility="collapsed",
    key="source_text_key" 
)

if st.button("Translate (Ctrl+Enter)", use_container_width=True, on_click=handle_translation, key="translate_btn"):
    if st.session_state.text_to_process:
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(st.session_state.text_to_process)

# --- RESULTS ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    all_selected = []
    
    for i, item in enumerate(st.session_state.translation_data["segments"]):
        segment_selections = render_segment_options(item, st.session_state.run_id, i)
        all_selected.extend(segment_selections)
        st.write("") 

    if all_selected:
        st.divider()
        st.code(" ".join(all_selected), language=None)

# --- UTILITIES ---
inject_keyboard_shortcut()