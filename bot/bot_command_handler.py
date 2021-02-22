class BaseCommandHandler:
    supported_commands = None

    def __init__(self, app):
        self.app = app

    def get_supported_commands(self):
        if self.supported_commands:
            return self.supported_commands
        raise NotImplementedError()

    def handle(self, client, message):
        raise NotImplementedError()

