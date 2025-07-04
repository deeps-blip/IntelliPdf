# 📄 IntelliPDF - AI Assistant for PDF Q&A

IntelliPDF is an intelligent desktop application that allows users to interact with PDF documents using natural language. Simply upload any PDF, ask questions, and receive accurate answers. The app uses multiple AI agents and a lightweight GUI built with PyQt6, integrated with Gemini and custom MCP decision logic.

---

## 🚀 Features

- 🧠 **AI-Powered Q&A** from PDF content
- 🗂 **Multi-Agent Verification** (e.g., PortalAgent, ToolAgent)
- 🤖 **MCP Engine**: Master Control Program to make smart decisions
- 🧵 **Threaded Response Handling**: App stays responsive during LLM calls
- 💾 **Persistent Uploads** in `data/uploads`
- 🖼️ **Sleek GUI** with icon-based PDF upload
- 🌗 **Dark Mode** Interface

---

## 📁 Project Structure

```yaml
IntelliPdf
├── main.py 
├── app/
│ ├── gui.py 
│ ├── controller.py 
│ ├── chat_history.py 
├── core/
│ ├── pdf_reader.py 
│ ├── llm_engine.py 
├── agents/
│ ├── base_agent.py
│ ├── portal_agent.py
│ ├── tool_agent.py
├── mcp/
│ ├── mcp_engine.py 
│ ├── strategies.py 
├── data/
│ ├── uploads/  
├── assets/
│ └── icons/ 
├── requirements.txt
└── README.md
```

---

## 🔧 Installation

### 📌 Requirements

- Python 3.10+
- [Gemini API key](https://makersuite.google.com/app)
- OS: Linux / Windows

### 📦 Install
```bash
git clone https://github.com/deeps-blip/IntelliPdf.git
cd IntelliPdf/
```

```bash
pip install -r requirements.txt
```
### ▶️ Run the App
```bash
python main.py
```
### 🔒 Compile to Binary (Using Nuitka)
- Make sure Nuitka is installed:

```bash
pip install nuitka
```
- Build as single .bin file

```bash
nuitka --standalone --onefile --enable-plugin=pyqt6 --follow-imports \
--include-data-dir=assets=assets \
--include-data-dir=data=data \
main.py

```
### 🌐 API Configuration
- Edit .env file in the root Directory
```env
GOOGLE_API_KEY=YOUR_API_KEY_OF_GEMINI
```
---
## 🛡 Security & Obfuscation
Use Nuitka instead of PyInstaller for better binary protection and performance.

Optional tools:

- pyarmor (lightweight obfuscation)

- cython + gcc (compile selective modules)
---
## 📃 License

Open for academic and personal use.

## 🙋‍♂️ Author

- Deepith A, Cybersecurity Enthusiast & Developer.
- Minimal. Fast. Practical.
---





