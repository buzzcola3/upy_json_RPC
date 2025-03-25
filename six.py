"""Utilities for writing code that runs on Python 3"""

import sys

__author__ = "Benjamin Peterson <benjamin@python.org>"
__version__ = "1.4.1"

string_types = str,
integer_types = int,
class_types = type,
text_type = str
binary_type = bytes

MAXSIZE = sys.maxsize

class _C:
    def _m(self):
        pass

class MovedAttribute(object):

    def __init__(self, name, new_mod, new_attr=None):
        self.name = name
        self.mod = new_mod
        self.attr = new_attr if new_attr else name

    def __get__(self, obj, tp):
        module = __import__(self.mod)
        result = getattr(module, self.attr)
        setattr(obj, self.name, result)
        return result


class _MovedItems(object):
    """Lazy loading of moved objects"""


_moved_attributes = [
    MovedAttribute("filter", "builtins", "filter"),
    MovedAttribute("map", "builtins", "map"),
    MovedAttribute("range", "builtins", "range"),
    MovedAttribute("zip", "builtins", "zip"),
]

for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)
del attr

moves = _MovedItems()


def add_move(move):
    """Add an item to six.moves."""
    setattr(_MovedItems, move.name, move)


def remove_move(name):
    """Remove item from six.moves."""
    try:
        delattr(_MovedItems, name)
    except AttributeError:
        raise AttributeError("no such move, %r" % (name,))


def get_unbound_function(unbound):
    return unbound


create_bound_method = type(_C()._m)


def iterkeys(d, **kw):
    """Return an iterator over the keys of a dictionary."""
    return iter(d.keys(**kw))

def itervalues(d, **kw):
    """Return an iterator over the values of a dictionary."""
    return iter(d.values(**kw))

def iteritems(d, **kw):
    """Return an iterator over the (key, value) pairs of a dictionary."""
    return iter(d.items(**kw))


def b(s):
    return s.encode("latin-1")

def u(s):
    return s

unichr = chr
int2byte = lambda i: bytes((i,))
byte2int = lambda bs: bs[0]
indexbytes = lambda buf, i: buf[i]
iterbytes = iter


def reraise(tp, value, tb=None):
    if value.__traceback__ is not tb:
        raise value.with_traceback(tb)
    raise value


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    return meta("NewBase", bases, {})

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper