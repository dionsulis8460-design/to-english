import streamlit as st
import streamlit.components.v1 as components

def inject_keyboard_shortcut():
    """Injects JS for shortcuts and a persistent tab title observer."""
    components.html(
        """
        <script>
        const doc = window.parent.document;
        const targetTitle = "BR ➡️ US";

        // 1. Force the title immediately
        doc.title = targetTitle;

        // 2. Persistent Observer to prevent Streamlit from reverting the title
        const titleObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (doc.title !== targetTitle) {
                    doc.title = targetTitle;
                }
            });
        });

        const titleNode = doc.querySelector('title');
        if (titleNode) {
            titleObserver.observe(titleNode, { subtree: true, characterData: true, childList: true });
        }

        // 3. Keyboard Shortcuts
        doc.addEventListener('keydown', function(e) {
            // Ctrl+Enter to Translate
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                const buttons = doc.querySelectorAll('button');
                for (const btn of buttons) {
                    if (btn.innerText.includes("Translate")) {
                        btn.click();
                        e.preventDefault();
                        break;
                    }
                }
            }

            // '/' to Focus Input
            if (e.key === '/' && 
                doc.activeElement.tagName !== 'TEXTAREA' && 
                doc.activeElement.tagName !== 'INPUT') {
                
                e.preventDefault(); 
                const textArea = doc.querySelector('textarea');
                if (textArea) {
                    textArea.focus();
                }
            }
        }, true);
        </script>
        """, height=0, width=0
    )

def render_segment_options(item, rid, segment_index):
    """Renders checkboxes for a specific translation segment."""
    selected = []
    v1_check = st.checkbox(item['v1'], key=f"r{rid}_s{segment_index}_v1")
    if v1_check: selected.append(item['v1'])
        
    v2_check = st.checkbox(item['v2'], key=f"r{rid}_s{segment_index}_v2")
    if v2_check: selected.append(item['v2'])
        
    v3_check = st.checkbox(item['v3'], key=f"r{rid}_s{segment_index}_v3")
    if v3_check: selected.append(item['v3'])
    
    return selected