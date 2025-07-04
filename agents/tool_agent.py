#pdf tool based agent
from agents.base_agent import BaseAgent
from core.llm_engine import call_gemini

class ToolAgent(BaseAgent):
    def verify(self):
        prompt = f"""
You are a tool data validation agent. The following PDF contains technical data about tools (e.g., GitHub, JIRA, VSCode). Please verify whether the tools and their usage descriptions look valid or realistic.

PDF Data:
{self.pdf_context}

List any mismatches, suspicious entries, or confirmations.
"""
        return call_gemini(prompt)
