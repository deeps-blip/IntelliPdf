import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QFileDialog, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSplashScreen
)
from PyQt6.QtGui import QFont, QTextCursor, QPixmap
from PyQt6.QtCore import Qt, QTimer
from app.controller import QAController  # Make sure this exists


class PDFQAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IntelliPDF - AI Assistant for PDF Q&A")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.pdf_text = ""
        self.controller = None

        # Title
        title = QLabel("IntelliPDF - Ask Your PDF")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Upload button
        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.setFont(QFont("Segoe UI", 13))
        self.upload_button.setStyleSheet("padding: 12px;")
        self.upload_button.clicked.connect(self.load_pdf)

        # File label
        self.file_label = QLabel("No file uploaded.")
        self.file_label.setStyleSheet("color: #bbb;")

        # Chat window
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setStyleSheet("background-color: #1e1e1e; color: white; padding: 10px;")
        self.answer_display.setFont(QFont("Segoe UI", 13))

        # Input field
        self.question_input = QLineEdit()
        self.question_input.setFont(QFont("Segoe UI", 13))
        self.question_input.setPlaceholderText("Ask a question based on the uploaded PDF")
        self.question_input.returnPressed.connect(self.answer_question)

        # Ask button
        self.ask_button = QPushButton("Ask")
        self.ask_button.setFont(QFont("Segoe UI", 13))
        self.ask_button.setStyleSheet("padding: 12px;")
        self.ask_button.clicked.connect(self.answer_question)
        self.ask_button.setEnabled(False)

        # Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.question_input)
        input_layout.addWidget(self.ask_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.answer_display)
        layout.addLayout(input_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.file_label.setText(f"Loaded PDF: {file_path.split('/')[-1]}")
            self.pdf_text = self.extract_text_from_pdf(file_path)
            self.controller = QAController(self.pdf_text)
            self.ask_button.setEnabled(True)
            self.append_message("PDF loaded successfully. Ask your question now.", sender="bot")

    def extract_text_from_pdf(self, path):
        text = ""
        for page in fitz.open(path):
            text += page.get_text()
        return text

    def answer_question(self):
        question = self.question_input.text().strip()
        if not question:
            return
        if not self.pdf_text or not self.controller:
            self.append_message("❗ No PDF loaded.", sender="bot")
            return

        self.append_message(question, sender="user")
        self.question_input.clear()

        try:
            answer = self.controller.ask(question)
        except Exception as e:
            answer = f"⚠️ Error: {str(e)}"

        self.append_message(answer, sender="bot")

    def append_message(self, text, sender='bot'):
        if sender == 'user':
            bubble = (
                "<div style='text-align: right; padding: 6px;'>"
                "<span style='background-color: #37474f; color: white; padding: 12px; border-radius: 10px; "
                "display: inline-block; max-width: 70%; font-size: 15px;'>"
                f"<b>You:</b> {text}"
                "</span></div>"
            )
        else:
            bubble = (
                "<div style='text-align: left; padding: 6px;'>"
                "<span style='background-color: #263238; color: #c3e88d; padding: 12px; border-radius: 10px; "
                "display: inline-block; max-width: 70%; font-size: 15px;'>"
                f"<b>AI:</b> {text}"
                "</span></div>"
            )
        self.answer_display.append(bubble)
        self.answer_display.moveCursor(QTextCursor.MoveOperation.End)


# Splash-related global vars
_splash = None
_splash_dots = 0
_splash_timer = None


def _update_splash_dots():
    global _splash_dots, _splash
    _splash_dots = (_splash_dots + 1) % 4
    dots = "." * _splash_dots
    if _splash:
        _splash.showMessage(f"Loading IntelliPDF{dots}",
                            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                            Qt.GlobalColor.white)


def launch_app():
    global _splash, _splash_timer
    app = QApplication(sys.argv)

    # Splash screen
    splash_pix = QPixmap(600, 300)
    splash_pix.fill(Qt.GlobalColor.black)
    _splash = QSplashScreen(splash_pix)
    _splash.setFont(QFont("Segoe UI", 18))
    _splash.showMessage("Loading IntelliPDF...",
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                        Qt.GlobalColor.white)
    _splash.show()

    # Animate dots
    _splash_timer = QTimer()
    _splash_timer.timeout.connect(_update_splash_dots)
    _splash_timer.start(500)

    # Load app after delay
    def show_main():
        window = PDFQAApp()
        window.show()
        _splash.finish(window)
        _splash_timer.stop()

    QTimer.singleShot(3000, show_main)
    sys.exit(app.exec())
