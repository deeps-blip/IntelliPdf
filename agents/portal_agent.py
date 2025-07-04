#interactive portal used agent
from agents.base_agent import BaseAgent
from core.llm_engine import call_gemini

class PortalAgent(BaseAgent):
    def verify(self):
        prompt = f"""
You are a portal verification agent. Analyze this PDF content to verify if all data related to portals (like access tokens, usernames, URLs, etc.) look correct, valid, and match typical patterns.

PDF Data:
{self.pdf_context}

Respond with a summary of validation results.
"""
        return call_gemini(prompt)
