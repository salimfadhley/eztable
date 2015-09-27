class Aggregation(object):

    def __init__(self, name, column_type, fn):
        self.name = name
        self.column_type = column_type
        self.fn = fn

    def __call__(self, t):
        return self.fn(t)
