# -*- coding: utf-8 -*-
"""
Contains the core serializer functionality.
"""
from __future__ import absolute_import

# stdlib imports
from collections import OrderedDict
from datetime import date as Date, datetime as Datetime
from logging import getLogger

# 3rd party imports
from jsobj import jsobj
from six import iteritems, string_types

# local imports
from .fieldspec import Fieldspec
from .util import iterable, is_file


L = getLogger(__name__)


def dump_val(name, value):
    """ The default implementation for object dump passed to jsobj. """
    if isinstance(value, (Date, Datetime)):
        return value.isoformat()
    return value


class Serializer(object):
    """ The serializer implementation

    This will serialize the object based on the fieldspec passed.

    Args:
        obj (anything):
            The serialized object. Whether the object will be serialized
            depends on if there is a serializer defined for that object.
        fieldspec (Fieldspec or str):
            Fieldspec according to which the object will be serialized.
        dumpval (Function):
            The value dumping function. This will be used to serialize
            primitive types.

    Returns:
        An object representation made only from primitive types. This can be
        passed to a function like json.dumps to dump it to a output format of
        choice.

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

    >>> from serafin import serialize
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

    Double wildcard (``**``) will expand all fields recursively. This is the
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

    def __init__(self):
        self.classmap = OrderedDict()

    def type(self, cls):
        """ Decorator for serializers that match strictly by type.

        Each type can have only one strict serializer associated with it.
        """
        def decorator(fn):      # pylint: disable=missing-docstring
            if cls in self.classmap:
                L.warning("Strict serializer already registered for {}".format(
                    cls.__name__
                ))
            self.classmap[cls] = fn
            return fn
        return decorator

    def __call__(self, obj, fieldspec='*', **kwargs):
        """ Serialize the object according to the given fieldspec.

        This is the method that should be used by the users of the lib.
        Compared to `raw_serialize()` it will convert fieldspec to a
        `Fieldspec` instance if necessary and build the serialization
        context based on the extra keyword arguments passed.

        :param Any obj:
        :param Fieldspec|unicode|str fieldspec:
        :param dict kwargs:
        :return dict.:
            Returns an object that can be directly dumped to JSON.
        """
        if isinstance(fieldspec, string_types):
            fieldspec = Fieldspec(fieldspec)
        elif fieldspec is None:
            fieldspec = Fieldspec('*')

        context = jsobj(
            dumpval=dump_val,
            reraise=True,
        )
        context.update(kwargs)

        return self.raw(obj, fieldspec, context)

    def raw(self, obj, fieldspec, context):
        """ Raw serialize without parsing the fieldspec.

        This method should be used when writing new serializers for performance
        reasons. When writing a new serializer you will already have a
        serialization context passed to the serializer function and the
        fieldspec will also already be passed as `Fieldspec` instance. Using
        `raw_serializer` will remove the overhead of creating those at
        each call level. The `serialize` method will create those when executed
        by the user code and then pass them to the serializer function. That
        function in turn might need to use other serializers defined elsewhere
        but won't need the overhead of calling `serialize()` again.

        :param Any obj:
        :param Fieldspec fieldspec:
        :param dict context:
        :return dict|list|str|int:
            Returns an object that can be directly dumped to JSON.
        """
        # Find serializer (inlined for performance reasons
        if obj is None:
            return None

        # Check if we have a direct serializer for the class
        try:
            serializer = self.classmap[obj.__class__]
        except KeyError:
            # Hacky speedups
            if isinstance(obj, dict):
                serializer = serialize_dict
            elif isinstance(obj, PRIMITIVES):
                serializer = serialize_primitive
            elif is_file(obj):
                serializer = serialize_file_handle
            elif iterable(obj):
                serializer = serialize_iterable
            elif callable(getattr(obj, 'serafin_serialize', None)):
                serializer = serialize_serializable
            else:
                # Look if we have direct serializer for a base class of obj
                for c, fn in iteritems(self.classmap):
                    if isinstance(obj, c):
                        serializer = fn
                        break
                else:
                    # Try if we can find 3rd party serializers.
                    if callable(getattr(obj, 'as_dict', None)):
                        serializer = ThirdPartySerializer('as_dict')
                    elif callable(getattr(obj, 'to_dict', None)):
                        serializer = ThirdPartySerializer('as_dict')
                    else:
                        # As a last resort try generic serialize_object
                        serializer = serialize_object

        # Do the actual serialization
        try:
            out = serializer(obj, fieldspec, context)
        except Exception as ex:
            out = "({}: {})".format(ex.__class__.__name__, str(ex))
            if context.reraise:
                raise

        return out


serialize = Serializer()


from .serializers import (     # noqa
    PRIMITIVES,
    serialize_dict,
    serialize_file_handle,
    serialize_iterable,
    serialize_object,
    serialize_primitive,
    serialize_serializable,
    ThirdPartySerializer,
)
