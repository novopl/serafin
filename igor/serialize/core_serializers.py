# -*- coding: utf-8 -*-
from __future__ import absolute_import
from logging import getLogger
from datetime import date as Date, datetime as Datetime
from decimal import Decimal
from itertools import chain
from six import integer_types, string_types, binary_type
from igor.js import jsobj
from igor.traits import iterable, isfileobj
from .base import serializer, fast_serializer, Priority
from .fieldspec import Fieldspec
L = getLogger(__name__)
PRIMITIVES = tuple(chain(
    integer_types,
    string_types,
    (float, binary_type, Date, Datetime, Decimal)
))


@serializer.add(Priority.HIGH, lambda o: isinstance(o, dict))
def serialize_dict(dct, fieldspec, dumpval, kwargs):
    """ Serialize dictionary. """
    ret = {}

    if not isinstance(fieldspec, Fieldspec):
        fieldspec = Fieldspec(fieldspec)

    if fieldspec.empty():
        return {}

    for name, value in dct.items():
        if name in fieldspec:
            try:
                ret[name] = serializer.serialize(value, fieldspec[name], dumpval,
                                                 **kwargs)
            except ValueError:
                pass
    return ret


@serializer.add(Priority.HIGH, lambda o: isinstance(o, PRIMITIVES))
def serialize_primitive(obj, fieldspec, dumpval, kwargs):
    return dumpval('', obj)


@serializer.add(Priority.HIGH, lambda o: o is None)
def serialize_None(obj, fieldspec, dumpval, kwargs):
    return None


@serializer.add(Priority.MEDIUM, lambda o: not isfileobj(o) and iterable(o))
def serialize_iterable(obj, fieldspec, dumpval, kwargs):
    if not isinstance(fieldspec, Fieldspec):
        fieldspec = Fieldspec(fieldspec)

    ret = []
    for item in obj:
        ret.append(serializer.serialize(item, fieldspec, dumpval, **kwargs))
    return ret


@serializer.add(Priority.MEDIUM, lambda o: isfileobj(o))
def serialize_file_handle(obj, fieldspec, dumpval, kwargs):
    return '(file handle)'

@serializer.add(
    Priority.MEDIUM,
    lambda o: hasattr(o, 'serialize') and hasattr(o.serialize, '__call__')
)
def serialize_serializable(obj, fieldspec, dumpval, kwargs):
    return obj.serialize()


@fast_serializer.add(Priority.LOW, lambda o: isinstance(o, object))
@serializer.add(Priority.LOW, lambda o: isinstance(o, object))
def serialize_object(obj, fieldspec, dumpval, kwargs):
    if not isinstance(fieldspec, Fieldspec):
        fieldspec = Fieldspec(fieldspec)

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
    reraise = kwargs.get('reraise', True)
    for name in dir(obj):
        if not isinstance(name, string_types):
            pass
        if name in fieldspec:
            try:
                value = getattr(obj, name)
            except Exception as ex:
                value = "({}: {})".format(ex.__class__.__name__, str(ex))
                if reraise:
                    raise

            if isval(name, value):
                ret[name] = serializer.serialize(value, fieldspec[name], dumpval,
                                                 **kwargs)
    return ret

