class Aggregation(object):

    def __init__(self, name, type, fn):
        self.name = name
        self.type = type
        self.fn = fn

    def __call__(self, t):
        return self.fn(t)
