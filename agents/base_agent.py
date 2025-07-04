#base agent used
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, pdf_context):
        self.pdf_context = pdf_context

    @abstractmethod
    def verify(self):
        """Return a verification summary or confidence score"""
        pass
