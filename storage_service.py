import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

def save_translation(text):
    """Saves a completed translation with a timestamp."""
    history = get_all_translations()
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": text
    }
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_all_translations():
    """Retrieves all saved translations."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def delete_translation(timestamp):
    """Removes a specific translation by its timestamp."""
    history = get_all_translations()
    updated_history = [entry for entry in history if entry['timestamp'] != timestamp]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_history, f, ensure_ascii=False, indent=2)

def clear_history():
    """Deletes all saved history."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)