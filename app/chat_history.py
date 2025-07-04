# app/chat_history.py

import json

class ChatHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, question, answer):
        self.history.append({
            "question": question,
            "answer": answer
        })

    def get_all(self):
        return self.history

    def clear(self):
        self.history = []

    def save_to_file(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            for i, entry in enumerate(self.history):
                f.write(f"Q{i+1}: {entry['question']}\n")
                f.write(f"A{i+1}: {entry['answer']}\n\n")

    def export_as_json(self):
        return json.dumps(self.history, indent=4, ensure_ascii=False)
