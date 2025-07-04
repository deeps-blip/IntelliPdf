from PyQt6.QtCore import QThread, pyqtSignal
from core.llm_engine import call_gemini  # your Gemini call function

class GeminiWorker(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        answer = call_gemini(self.prompt)
        self.result_ready.emit(answer)
