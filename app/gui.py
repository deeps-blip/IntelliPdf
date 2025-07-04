import sys
import fitz
import threading
import os
from shutil import copyfile

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QLabel,
    QFileDialog, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QSplashScreen,
    QToolButton, QSizePolicy
)
from PyQt6.QtGui import QFont, QTextCursor, QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer, QSize

from app.controller import QAController


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
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Upload button with icon
        self.upload_button = QToolButton()
        self.upload_button.setIcon(QIcon("assets/icons/upload.png"))
        self.upload_button.setIconSize(QSize(64, 64))
        self.upload_button.setText("Upload PDF")
        self.upload_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.upload_button.setStyleSheet(
            "padding: 16px; color: white; background-color: #1e1e1e; border: 1px solid #333;")
        self.upload_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.upload_button.clicked.connect(self.load_pdf)

        self.file_label = QLabel("No file uploaded.")
        self.file_label.setStyleSheet("color: #bbb;")

        # Chat window
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setStyleSheet(
            "background-color: #121212; color: white; padding: 10px; font-size: 14px;"
        )

        # Question input
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Ask a question based on the uploaded PDF")
        self.question_input.setStyleSheet("font-size: 14px; padding: 8px;")
        self.question_input.returnPressed.connect(self.answer_question)

        # Ask button
        self.ask_button = QPushButton("Ask")
        self.ask_button.setEnabled(False)
        self.ask_button.setFixedHeight(40)
        self.ask_button.setStyleSheet("background-color: #1e88e5; color: white; font-size: 14px;")
        self.ask_button.clicked.connect(self.answer_question)

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
            upload_folder = "data/uploads"
            os.makedirs(upload_folder, exist_ok=True)

            filename = os.path.basename(file_path)
            dest_path = os.path.join(upload_folder, filename)
            copyfile(file_path, dest_path)

            self.file_label.setText(f"Loaded PDF: {filename}")
            self.pdf_text = self.extract_text_from_pdf(dest_path)
            self.controller = QAController(self.pdf_text)
            self.ask_button.setEnabled(True)
            self.append_message("PDF loaded successfully. Ask your question now.", sender="AI")

            # Run agent verification in background
            threading.Thread(target=self.run_agent_verification).start()

    def extract_text_from_pdf(self, path):
        text = ""
        for page in fitz.open(path):
            text += page.get_text()
        return text

    def answer_question(self):
        question = self.question_input.text().strip()
        if not question or not self.pdf_text or not self.controller:
            self.append_message("❗ No PDF loaded.", sender="AI")
            return

        self.append_message(question, sender="You")
        self.question_input.clear()
        self.append_message("Processing...", sender="AI")

        def get_answer():
            try:
                answer = self.controller.ask(question)
            except Exception as e:
                answer = f"⚠️ Error: {str(e)}"

            self.remove_last_message()
            self.append_message(answer, sender="AI")

        threading.Thread(target=get_answer).start()

    def run_agent_verification(self):
        self.append_message("🔍 Verifying PDF with available agents...", sender="AI")
        self.answer_display.append("<hr>")

        try:
            verification = self.controller.verify_pdf_with_agents()
            for agent, result in verification.items():
                self.append_message(f"{agent} says:\n{result}", sender="AI")
        except Exception as e:
            self.append_message(f"⚠️ Agent verification failed: {str(e)}", sender="AI")

    def append_message(self, text, sender='AI'):
        color = "#c3e88d" if sender == "AI" else "#80cbc4"
        spacing = "margin-top: 10px; margin-bottom: 10px;"
        bubble = (
            f"<div style='text-align: left; {spacing}'>"
            f"<span style='color: {color}; font-weight: bold;'>{sender}:</span><br>"
            f"<span style='padding: 6px; display: inline-block; max-width: 70%;'>{text}</span>"
            f"</div>"
        )
        self.answer_display.append(bubble)
        self.answer_display.moveCursor(QTextCursor.MoveOperation.End)

    def remove_last_message(self):
        cursor = self.answer_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
        self.answer_display.setTextCursor(cursor)


# Splash screen functionality
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

    splash_pix = QPixmap(600, 300)
    splash_pix.fill(Qt.GlobalColor.black)
    _splash = QSplashScreen(splash_pix)
    _splash.setFont(QFont("Segoe UI", 18))
    _splash.showMessage("Loading IntelliPDF...",
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
                        Qt.GlobalColor.white)
    _splash.show()

    _splash_timer = QTimer()
    _splash_timer.timeout.connect(_update_splash_dots)
    _splash_timer.start(500)

    def show_main():
        window = PDFQAApp()
        window.show()
        _splash.finish(window)
        _splash_timer.stop()

    QTimer.singleShot(3000, show_main)
    sys.exit(app.exec())
