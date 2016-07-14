# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import OrderedDict
from logging import getLogger
from datetime import date as Date, datetime as Datetime
from decimal import Decimal
from itertools import chain
from six import integer_types, string_types, binary_type
from igor.js import jsobj
from igor.traits import iterable, isfileobj
from .base import serializer, Priority
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

    if fieldspec == True or fieldspec.empty():
        return {}

    for name, value in dct.items():
        if name in fieldspec:
            try:
                ret[name] = serializer.raw_serialize(value, fieldspec[name], context)
            except ValueError:
                pass
    return ret


@serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, PRIMITIVES))
def serialize_primitive(obj, fieldspec, context):
    return context.dumpval('', obj)


@serializer.fuzzy(Priority.HIGH, lambda o: o is None)
def serialize_None(obj, fieldspec, context):
    return None


@serializer.strict(list)
@serializer.strict(tuple)
@serializer.fuzzy(Priority.MEDIUM, lambda o: not isfileobj(o) and iterable(o))
def serialize_iterable(obj, fieldspec, context):
    ret = []
    for item in obj:
        ret.append(serializer.raw_serialize(item, fieldspec, context))
    return ret


@serializer.fuzzy(Priority.MEDIUM, lambda o: isfileobj(o))
def serialize_file_handle(obj, fieldspec, context):
    return '(file handle)'

@serializer.fuzzy(
    Priority.MEDIUM,
    lambda o: hasattr(o, 'serialize') and hasattr(o.serialize, '__call__')
)
def serialize_serializable(obj, fieldspec, context):
    return obj.serialize(fieldspec, context)


@serializer.fuzzy(Priority.LOW, lambda o: isinstance(o, object))
def serialize_object(obj, fieldspec, context):
    if fieldspec.empty():
        return {}

    filters = [
        lambda n, v: not (n.startswith('__') or n.endswith('__')),
        lambda n, v: not callable(v),
        lambda n, v: not isfileobj(v),
    ]

    def isval(attrname, attrvalue):
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
                ret[name] = serializer.raw_serialize(value, fieldspec[name], context)
    return ret

