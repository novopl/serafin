# -*- coding: utf-8 -*-
from __future__ import absolute_import
from collections import OrderedDict
from datetime import date as Date, datetime as Datetime
from igor.enum import Enum
from igor.traits import iterable, isfileobj
from igor.js import jsobj
from six import iteritems, string_types
from .fieldspec import Fieldspec


class Priority(Enum):
    """
    **HIGH**
        Serializers matching (almost) exactly, very strict. The client code
        should assume, that the serializer implements perfect or near perfect
        serialization for all of it's matching types.

    **MEDIUM**
        Serializer is able to do a decent job at serializing its input values.
        This priority should be used for a more general type matchers and as
        a "decent polyfill" - Means it can be improved, but it's working well
        for now.

    **LOW**
        This priority should be used by all serializers that match a wide
        range of types. In most cases this will be used as a fallback, i.e. no
        serializers with higher priority (better support for the type) match.
    """
    HIGH    = 100
    MEDIUM  = 50
    LOW     = 0


def dumpval(name, value):
    if isinstance(value, (Date, Datetime)):
        return value.isoformat()
    return value


class Serializer(object):
    """
    HIGH priority is for serializers with a strict selector.

    >>> @serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, Model))
    ... def serialize_model(model, fieldspec, dumpval, kwargs):
    ...     pass

    >>> @serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, dict))
    ... def serialize_dict(model, fieldspec, dumpval, kwargs):
    ...     pass

    >>> @serializer.fuzzy(Priority.HIGH, lambda o: isinstance(o, jsobj))
    ... def serialize_jsobj(model, fieldspec, dumpval, kwargs):
    ...     pass

    >>> @serializer.fuzzy(Priority.HIGH,
    ...     lambda o: isinstance(o, (int, float, str, unicode, bytes))
    ... )
    ... def serialize_primitive(model, fieldspec, dumpval, kwargs):
    ...     pass

    MEDIUM priority since this will catch every iterable, and we might want
    a more custom serializer.

    >>> @serializer.fuzzy(Priority.MEDIUM, lambda o: iterable(o))
    ... def serialize_iterable(model, fieldspec, dumpval, kwargs):
    ...     pass

    Low because it will catch almost everything. This is a kind of general
    fallback if we don't have specialized serializer.

    >>> @serializer.fuzzy(Priority.LOW, lambda o: isinstance(o, object))
    ... def serialize_object(model, fieldspec, dumpval, kwargs):
    ...     pass
    """

    def __init__(self):
        self.serializers = {}
        self.classmap = OrderedDict()

    def strict(self, cls):
        def decorator(fn):
            self.classmap[cls] = fn
            return fn
        return decorator

    def fuzzy(self, priority, check):
        def decorator(fn):
            """
            >>> ismodel = lambda o: isinstance(o, Model)
            >>> @serializer.fuzzy.fuzzy(Priority.HIGH, ismodel)
            ... def serialize_model(model, fieldspec, dumpval, kwargs):
            ...     # ...
            """
            fn._serializer_priority  = priority
            fn._serializer_check     = check
            if priority not in self.serializers:
                self.serializers[priority] = [fn]
            else:
                self.serializers[priority].append(fn)
            return fn

        return decorator

    def raw_serialize(self, obj, fieldspec, context):
        serializer = self.find(obj)
        try:
            out = serializer(obj, fieldspec, context)
        except Exception as ex:
            out = "({}: {})".format(ex.__class__.__name__, str(ex))
            if context.reraise:
                raise
        return out

    def serialize(self, obj, fieldspec='*', **kwargs):
        if isinstance(fieldspec, string_types):
            fieldspec = Fieldspec(fieldspec)
        elif fieldspec is None:
            fieldspec = Fieldspec('*')

        context = jsobj(
            dumpval=dumpval,
            reraise=True,
        )
        context.update(kwargs)

        return self.raw_serialize(obj, fieldspec, context)

    def find_by_priority(self, obj, minpriority=Priority.LOW):
        """ Find serializer for the fiven object.

        :param obj:
            The object you want the serializer for.

        :param minpriority:
            The minimum priority of the serializer. Serializers with lower priority
            won't be returned. This allows to exclude fallback serializers from the
            search.
        :type minpriority: Priority

        :returns:
            Serializer function if found or ``None``.
        """
        serializer = None
        for priority in sorted(self.serializers.keys(), key=lambda x: -x):
            if priority >= minpriority:
                for s in self.serializers[priority]:
                    if s._serializer_check(obj):
                        serializer = s
                        break
                else:
                    continue
                break
        else:
            raise ValueError("Don't know how to serialize {}".format(
                str(type(obj))
            ))
        return serializer

    def find(self, obj, minpriority=Priority.LOW):
        if obj is None:
            return None

        cls = obj.__class__
        # Check if we have a direct serializer for the class
        serializer = self.classmap.get(cls)
        if serializer is not None:
            return serializer

        # Hacky speedups
        if isinstance(obj, dict):
            return serialize_dict
        if isinstance(obj, PRIMITIVES):
            return serialize_primitive
        if isfileobj(obj):
            return serialize_file_handle
        if iterable(obj):
            return serialize_iterable
        if hasattr(obj, 'serialize') and hasattr(obj.serialize, '__call__'):
            return serialize_serializable

        # Look if we have direct serializer for a base class of obj
        for c, serializer in iteritems(self.classmap):
            if isinstance(obj, c):
                return serializer

        return self.find_by_priority(minpriority)



serializer = Serializer()


def serialize(obj, fieldspec=None, **context):
    """ This will serialize the object based on the fieldspec passed.

    Args:
        obj (anything):     The serialized object. Whether the object will be serialized
                            depends on if there is a serializer defined for that object.
        fieldspec (Fieldspec or str):
           Fieldspec according to which the object will be serialized.
        dumpval (Function): The value dumping function. This will be used to serialize
                            primitive types.

    Returns:
        An object representation made only from primitive types. This can be passed to a
        function like json.dumps to dump it to a output format of choice.

    **Examples**

    With the following data (same applies to django models and ``jsobj``):

    >>> model = {
    ...     'field1': 10,
    ...     'field2': {
    ...         'sub1': 1,
    ...         'sub2': 2,
    ...     },
    ...     'field3': 20,
    ... }

    Here are a few examples of what fields would be selected by each
    fieldspec (second argument for ``serialize``):

    >>> from igor.serialize import serialize
    >>> serialize(model, '*') == {
    ...     'field1': 10,
    ...     'field2': {},
    ...     'field3': 20
    ... }
    True

    Serialize only selected fields.

    >>> serialize(model, 'field1,field3') == {
    ...     'field1': 10,
    ...     'field3': 20
    ... }
    True

    Specify what fields to expand on an object.

    >>> serialize(model, 'field1,field2(sub1)') == {
    ...     'field1': 10,
    ...     'field2': {
    ...         'sub1': 1
    ...     }
    ... }
    True

    Wildcards (``*``) expand all fields for that given object, *without*
    expanding nested objects.

    >>> serialize(model, 'field1,field2(*)') == {
    ...     'field1': 10,
    ...     'field2': {
    ...         'sub1': 1,
    ...         'sub2': 2
    ...     }
    ... }
    True

    Double wirldcard (``**``) will expand all fields recursively. This is the
    most heavy call.

    >>> serialize(model, '**') == {
    ...     'field1': 10,
    ...     'field2': {
    ...         'sub1': 1,
    ...         'sub2': 2
    ...     },
    ...     'field3': 20
    ... }
    True

    """
    return serializer.serialize(obj, fieldspec, **context)


from .core_serializers import (
    serialize_dict, serialize_file_handle, serialize_iterable,
    serialize_primitive, serialize_serializable,
    PRIMITIVES,
)
