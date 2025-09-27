

class MetaTraderIOException(Exception):

    def __init__(self, message: str, code : int) -> None:
        self.code = code
        super().__init__(f"(msg: {message}, code: {code})")


class MetaTraderStreamingException(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.code = code
        super().__init__(f"(msg: {message}, code: {code})")