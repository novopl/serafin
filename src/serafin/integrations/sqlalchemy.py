# -*- coding: utf-8 -*-
""" Serafin integration with SQLAlchemy. """
from __future__ import absolute_import, unicode_literals

# local imports
from serafin import serialize
from serafin.core import util


def make_serializer(model_base_class):
    """ Create serialize for the given SQLAlchemy base model class.

    This is the class you get by calling SQLAlchemy's declarative_base()
    """
    @serialize.type(model_base_class)
    def serialize_flask_model(obj, spec, ctx):
        """ serafin serializer for ndb models. """
        if spec is True or spec.empty():
            return {}

        props = list(util.iter_public_props(obj, lambda n, v: n in spec))
        ret = {}

        ret.update(_serialize_flask_model_fields(obj, spec, ctx))
        ret.update({k: serialize.raw(val, spec[k], ctx) for k, val in props})

        return ret

    return serialize_flask_model


def _serialize_flask_model_fields(model, spec, ctx):
    """ Serialize SQLAlchemy model class fields. """
    ret = {}

    columns = model.__table__.columns.items()

    for name, _ in columns:
        if name in spec:
            value = getattr(model, name)
            ret[name] = serialize.raw(value, spec[name], ctx)

    return ret
