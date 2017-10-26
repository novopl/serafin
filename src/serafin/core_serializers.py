# -*- coding: utf-8 -*-
"""
Built-in serializers for most basic uses cases.

Those are provided as they would have to be reimplemented time and time again
by each project. Having them as part of the library will also allow some
performance optimisation in the `Serializer` itself.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from collections import OrderedDict
from datetime import date as Date, datetime as Datetime
from decimal import Decimal
from itertools import chain
from logging import getLogger

# 3rd party imports
from jsobj import jsobj
from six import integer_types, string_types, binary_type

# local imports
from .core import serializer, Priority
from .util import iterable, isfile


L = getLogger(__name__)
PRIMITIVES = tuple(chain(
    integer_types,
    string_types,
    (float, binary_type, Date, Datetime, Decimal)
))


@serializer.strict(OrderedDict)
@serializer.strict(dict)
@serializer.strict(jsobj)
@serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, dict))
def serialize_dict(dct, fieldspec, context):
    """ Serialize dictionary. """
    ret = {}

    if fieldspec is True or fieldspec.empty():
        return {}

    for name, value in dct.items():
        if name in fieldspec:
            try:
                ret[name] = serializer.raw_serialize(
                    value, fieldspec[name], context
                )
            except ValueError:
                pass
    return ret


@serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, PRIMITIVES))
def serialize_primitive(obj, fieldspec, context):
    """ Serialize a primitive value. """
    return context.dumpval('', obj)


@serializer.strict(list)
@serializer.strict(tuple)
@serializer.fuzzy(Priority.MEDIUM, lambda o: not isfile(o) and iterable(o))
def serialize_iterable(obj, fieldspec, context):
    """ Serialize any iterable except a string.

    Since strings are a very special case of iterables, they are handled
    differently (otherwise they would be serialized as an array of chars).
    """
    ret = []
    for item in obj:
        ret.append(serializer.raw_serialize(item, fieldspec, context))
    return ret


@serializer.fuzzy(Priority.MEDIUM, lambda o: isfile(o))
def serialize_file_handle(obj, fieldspec, context):
    """ Serializer for file handles. """
    return '(file handle)'


@serializer.fuzzy(
    Priority.MEDIUM,
    lambda o: hasattr(o, 'serialize') and hasattr(o.serialize, '__call__')
)
def serialize_serializable(obj, fieldspec, context):
    """ Serialize any class that defines a ``serialize`` method. """
    return obj.serialize()


@serializer.fuzzy(Priority.LOW, lambda o: isinstance(o, object))
def serialize_object(obj, fieldspec, context):
    """ Serialize any object.

    This should have the lowest priority as it will work for almost anything
    but it might be a bit slow. It's generally much better to use other,
    dedicated, serializers and leave this as a last resort. Having this makes
    the system very flexible but at the same time it might slow down the
    serialization time significantly.
    """
    if fieldspec is True or fieldspec.empty():
        return {}

    filters = [
        lambda n, v: not (n.startswith('__') or n.endswith('__')),
        lambda n, v: not callable(v),
        lambda n, v: not isfile(v),
    ]

    def isval(attrname, attrvalue):
        """
        Check if the given attribute is a value that should be serialized.
        """
        try:
            return all(flt(attrname, attrvalue) for flt in filters)
        except:
            return False

    ret = {}
    for name in dir(obj):
        if not isinstance(name, string_types):
            pass
        if name in fieldspec:
            try:
                value = getattr(obj, name)
            except Exception as ex:
                value = "({}: {})".format(ex.__class__.__name__, str(ex))
                if context.reraise:
                    raise

            if isval(name, value):
                ret[name] = serializer.raw_serialize(
                    value, fieldspec[name], context
                )
    return ret
