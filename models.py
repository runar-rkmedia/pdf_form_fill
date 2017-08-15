"""Database-structure for item-catalog."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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
