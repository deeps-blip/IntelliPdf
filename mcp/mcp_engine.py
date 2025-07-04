#mcp engine used

from mcp.strategies import SimpleKeywordStrategy

class MCPEngine:
    def __init__(self):
        self.strategy = SimpleKeywordStrategy()

    def select_agents(self, context_text: str) -> list:
        """Select relevant agents based on strategy."""
        return self.strategy.choose_agents(context_text)
