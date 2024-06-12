class CantParseSchema(Exception):
    def __init__(self, message: str = "Undefined exception"):
        super().__init__(message)


class CantGenerateSchema(Exception):
    def __init__(self, message: str = "Undefined exception"):
        super().__init__(message)


class CantValidateValue(Exception):
    def __init__(self, message: str = "Undefined exception"):
        super().__init__(message)
