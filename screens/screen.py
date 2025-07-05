from abc import ABC, abstractmethod

class Screen(ABC):
    def __init__(self, app):
        self.app = app
        self.popups = []

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_input(self):
        pass

