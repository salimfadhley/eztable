class InvalidSchema(TypeError):
    """Raised when a schema appears to be invalid
    """

class InvalidColumn(TypeError):
    """Raised when a column in a schema appears to be invalud
    """

class InvalidData(TypeError):
    """Raised when an insert cannot complete because the row does not conform
    to the schema
    """