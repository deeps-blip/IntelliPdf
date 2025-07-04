#diff strats
from agents.portal_agent import PortalAgent
from agents.tool_agent import ToolAgent

class SimpleKeywordStrategy:
    def choose_agents(self, context_text: str) -> list:
        selected = []

        # Example logic: Check for specific keywords
        if "portal" in context_text.lower():
            selected.append(PortalAgent(context_text))

        if "tool" in context_text.lower() or "github" in context_text.lower():
            selected.append(ToolAgent(context_text))

        # If no keywords matched, load both (fallback)
        if not selected:
            selected = [
                PortalAgent(context_text),
                ToolAgent(context_text)
            ]

        return selected
