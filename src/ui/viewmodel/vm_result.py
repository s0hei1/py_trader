from dataclasses import dataclass


@dataclass
class VMResult:
    has_error : bool = False
    message : str = "Sucessful operation"