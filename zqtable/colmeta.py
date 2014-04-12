from .exceptions import InvalidColumn, InvalidSchema

class ColMeta(object):

    def __init__(self, name, col_type, allow_none=True):
        if not isinstance(name, str):
            raise InvalidColumn('Bad name: %s (%r)' % (name, name))
        if not isinstance(col_type, type):
            raise InvalidColumn('Bad type: %r' % col_type)

        self.name = name
        self.col_type = col_type
        self.allow_none = allow_none

    def __eq__(self, other):
        return self.name == other.name and self.col_type == other.col_type

    def validate(self, obj):
        if self.allow_none and obj == None:
            return True
        return isinstance(obj, self.col_type)

    def __str__(self):
        if self.col_type == str:
            return self.name
        else:
            return '%s (%s)' % (self.name, self.col_type.__name__)

    def __repr__(self):
        return "<%s.%s %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            str(self)
        )
