"""

``igor.serialize`` is a serialization system that allows flexible serialization of any
type of object according to a provided fieldspec. The fieldspec tells the serialize which
attribute/fields/members of the given object should be serialized. This allows for a very
flexible serialization system, especialy in the context of API endpoints where we can
write one endpoint and allow client to pass the fieldspec describing how he wants the
output to be formatted.


.. autoclass:: igor.serialize.base.Priority
    :members:


.. autoclass:: igor.serialize.base.Serializer
    :members:


.. autofunction:: igor.serialize.base.serialize

"""
from .base import Priority, serializer, serialize
from .core_serializers import *
__all__ = [
    'Priority',
    'serializer',
    'serialize'
]
