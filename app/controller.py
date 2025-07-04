from agents.portal_agent import PortalAgent
from agents.tool_agent import ToolAgent
from core.llm_engine import call_gemini

class QAController:
    def __init__(self, context_text):
        self.context = context_text
        self.portal_agent = PortalAgent(context_text)
        self.tool_agent = ToolAgent(context_text)

    def ask(self, question: str) -> str:
        prompt = f"""Use the following PDF content to answer the question.

PDF Content:
{self.context}

Question: {question}
Answer:"""
        return call_gemini(prompt)

    def verify_pdf_with_agents(self) -> dict:
        """Verify PDF content using all available agents."""
        return {
            "PortalAgent": self.portal_agent.verify(),
            "ToolAgent": self.tool_agent.verify()
        }
