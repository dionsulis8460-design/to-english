import streamlit as st
from translator_service import get_segmented_translations
from ui_components import inject_keyboard_shortcut, render_segment_options
from storage_service import save_translation, get_all_translations, delete_translation

# --- CALLBACKS ---
def handle_translation():
    """Manages input clearing and state resets for a new translation run."""
    if st.session_state.source_text_key.strip():
        st.session_state.text_to_process = st.session_state.source_text_key
        st.session_state.source_text_key = ""
        st.session_state.translation_data = None
        st.session_state.run_id += 1
    else:
        st.session_state.text_to_process = None

# --- APP INITIALIZATION ---
st.set_page_config(page_title="Translator", layout="centered")

# CSS to force text wrapping in st.code and make the sidebar buttons discreet
st.markdown("""
    <style>
    /* Force st.code to wrap lines instead of horizontal scrolling */
    code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    /* Make the sidebar delete buttons look like small links */
    .stSidebar button {
        border: none !important;
        background-color: transparent !important;
        color: #888 !important;
        padding: 0 !important;
        font-size: 0.8rem !important;
        float: right;
    }
    .stSidebar button:hover {
        color: #ff4b4b !important;
        text-decoration: underline !important;
    }
    </style>
""", unsafe_allow_html=True)

if "translation_data" not in st.session_state:
    st.session_state.translation_data = None
if "text_to_process" not in st.session_state:
    st.session_state.text_to_process = None
if "run_id" not in st.session_state:
    st.session_state.run_id = 0

# --- SIDEBAR HISTORY ---
with st.sidebar:
    saved_texts = get_all_translations()
    for entry in saved_texts:
        # Display the copyable code block (wrapping is now forced via CSS)
        st.code(entry['content'], language=None)
        
        # Discreet Delete Button below each box
        if st.button("Delete entry", key=f"del_{entry['timestamp']}"):
            delete_translation(entry['timestamp'])
            st.rerun()
        
        st.write("") # Small spacer between entries

# --- USER INPUT ---
st.text_area(
    "Source:", 
    placeholder="...", 
    height=150, 
    label_visibility="collapsed",
    key="source_text_key" 
)

if st.button("Translate", use_container_width=True, on_click=handle_translation, key="translate_btn"):
    if st.session_state.text_to_process:
        with st.spinner("Processing..."):
            st.session_state.translation_data = get_segmented_translations(st.session_state.text_to_process)
    else:
        st.warning("Por favor, insira um texto.")

# --- RESULTS & SELECTION ---
if st.session_state.translation_data and "segments" in st.session_state.translation_data:
    st.divider()
    all_selected = []
    
    for i, item in enumerate(st.session_state.translation_data["segments"]):
        segment_selections = render_segment_options(item, st.session_state.run_id, i)
        all_selected.extend(segment_selections)
        st.write("")

    if all_selected:
        st.divider()
        final_text = " ".join(all_selected)
        st.code(final_text, language=None)
        
        if st.button("💾", use_container_width=True):
            save_translation(final_text)
            st.rerun()

inject_keyboard_shortcut()