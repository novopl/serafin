# -*- coding: utf-8 -*-
""" AppEngine ndb integration """
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from google.appengine.ext import ndb

# local imports
from serafin.core import util
from serafin.core.serializer import serialize


@serialize.type(ndb.Model)
def serialize_ndb_model(obj, spec, ctx):
    """ serafin serializer for ndb models. """
    if spec is True or spec.empty():
        return {}

    ret = {'id': obj.key.id()}
    props = list(util.iter_public_props(obj, lambda n, v: n in spec))

    ret.update(serialize_ndb_props(obj, spec, ctx))
    ret.update({key: serialize.raw(val, spec[key], ctx) for key, val in props})

    return ret


def serialize_ndb_props(model, fieldspec, ctx):
    """ Serialize properties on a ndb.Model

    :param ndb.Model model:
        The model we want to serialize.
    :param Fieldspec fieldspec:
        Defines what fields will be included in the result.
    :param Context context:
        Serialization context. For more information, refer to **serafin**
        documentation.
    :return dict:
        A dictionary containing the serialized data. The layout of the
        dictionary will depend on the fieldspec passed.
    """
    data = {}

    for prop in model._properties.itervalues():
        name = prop._code_name

        if name in fieldspec:
            value = prop._get_for_dict(model)

            if isinstance(value, ndb.Key):
                name += '_id'
                value = value.id()

            data[name] = serialize.raw(value, fieldspec[name], ctx)

    return data
