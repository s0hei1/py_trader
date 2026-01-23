class VMException(Exception):

    def __init__(self, message : str = 'There was No messages'):
        self.message = message
        super().__init__(self.message)