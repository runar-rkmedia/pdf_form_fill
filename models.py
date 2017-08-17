"""Database-structure for item-catalog."""

from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal
from datetime import datetime
from flask import json


class MyJSONEncoder(json.JSONEncoder):
    """Redefine flasks json-encoded to convert Decimals.."""

    def default(self, obj):  # noqa
        if isinstance(obj, Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(MyJSONEncoder, self).default(obj)

    def _iterencode(self, o, markers=None):
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(MyJSONEncoder, self)._iterencode(o, markers)


json.JSONEncoder = MyJSONEncoder


class MySQLAlchemy(SQLAlchemy):

    def apply_driver_hacks(self, app, info, options):
        # add options here
        options.update(json_serializer=json.dumps,)
        super().apply_driver_hacks(app, info, options)


db = MySQLAlchemy()

PER_PAGE = 500


class ByID(object):
    """Class which can return it's entity by id."""
    @classmethod
    def by_id(cls, this_id):
        """Return a entity by its id."""
        try:
            this_id = int(this_id)
        except (ValueError, TypeError):
            return None
        entity = cls.query.filter(cls.id == this_id).first()
        if not entity:
            return None
        return entity


class MyBaseModel(ByID):
    """Basic functionality."""

    def owns(self, user):
        """Check if owner."""
        raise NotImplementedError("{} missing owns-method".format(type(self)))

    @classmethod
    def by_id(cls, this_id, user):
        """Return a entity by its id."""
        entity = super(MyBaseModel, cls).by_id(this_id)
        if entity:
            entity.owns(user)
            return entity

    def update_entity(self, dictionary):
        """Update an entity from a dictionary."""
        for key, val, in dictionary.items():
            setattr(self, key, val)
        return self


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoAccess(Error):
    '''
    Raise when a user doesn't have access to the action or resource

    https://stackoverflow.com/a/26938914/3493586
    '''

    def __init__(self, message, *args):
        self.message = message
        super(NoAccess, self).__init__(message, *args)
