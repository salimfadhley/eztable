class InvalidSchema(TypeError):
    """Raised when a schema appears to be invalid"""


class InvalidColumn(TypeError):
    """Raised when a column in a schema appears to be invalid"""


class InvalidData(TypeError):
    "An insert cannot complete because the row does not conform to the schema"


class InvalidIndex(ValueError):
    """An index cannot be created because it has no columns or it refers to
    columns which do not exist in it's table."""

class InvalidJoinMode(KeyError):
    """The requested join mode is not knowm"""
