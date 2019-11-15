class MismatchedBracketsError(Exception):
    """Raised when there is a incomplete pair of brackets"""
    pass


class MemoryOutOfBoundsError(Exception):
    """Raised when the pointer goes beyond either end of the memory cells"""
    pass
