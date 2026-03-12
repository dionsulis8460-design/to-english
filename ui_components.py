import streamlit as st
import streamlit.components.v1 as components

def inject_keyboard_shortcut():
    """Injects JavaScript for shortcuts: Ctrl+Enter (Translate) and '/' (Focus Input)."""
    components.html(
        """
        <script>
        const doc = window.parent.document;

        doc.addEventListener('keydown', function(e) {
            // 1. Keyboard Shortcut (Ctrl+Enter or Cmd+Enter) to Translate
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const buttons = doc.querySelectorAll('button');
                for (const btn of buttons) {
                    // Check for the specific button text
                    if (btn.innerText.includes("Translate")) {
                        btn.click();
                        e.preventDefault();
                        break;
                    }
                }
            }

            // 2. Keyboard Shortcut ('/') to Focus Input
            // Only trigger if we aren't already in an input/textarea
            if (e.key === '/' && 
                doc.activeElement.tagName !== 'TEXTAREA' && 
                doc.activeElement.tagName !== 'INPUT') {
                
                e.preventDefault(); 
                const textArea = doc.querySelector('textarea');
                if (textArea) {
                    textArea.focus();
                }
            }
        }, true); // Using 'true' for capture phase to catch events early
        </script>
        """, height=0, width=0
    )

def render_segment_options(item, rid, segment_index):
    """Renders the three checkboxes for a specific translation segment."""
    selected = []
    v1_check = st.checkbox(item['v1'], key=f"r{rid}_s{segment_index}_v1")
    if v1_check: selected.append(item['v1'])
        
    v2_check = st.checkbox(item['v2'], key=f"r{rid}_s{segment_index}_v2")
    if v2_check: selected.append(item['v2'])
        
    v3_check = st.checkbox(item['v3'], key=f"r{rid}_s{segment_index}_v3")
    if v3_check: selected.append(item['v3'])
    
    return selected