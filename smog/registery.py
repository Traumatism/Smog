class Registery:
    def __init__(self):
        self.modules = []

    def add_module(self, module) -> None:
        self.modules.append(module)
