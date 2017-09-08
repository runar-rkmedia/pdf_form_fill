"""Custom exceptions."""
from enum import Enum


class DefconLevel(Enum):
    # Really just a bootstrap-color-type
    default = 5
    successs = 4
    info = 3
    warning = 2
    danger = 1


class MyBaseException(Exception):
    status_code = 400
    message = 'Feil.'
    defcon_level = DefconLevel.warning

    def __init__(self,
                 message=None,
                 status_code=None,
                 defcon_level=None,
                 payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['errors'] = [{
            'message': self.message,
            'defcon_level': self.defcon_level.value
        }]
        return rv


class LocationException(MyBaseException):
    status_code = 401
    defcon_level = DefconLevel.warning
    message = 'Kunne ikke finne denne adressen.'


class NotAuthorized(MyBaseException):
    status_code = 401
    defcon_level = DefconLevel.warning
    message = 'Du har ikke tilgang til denne ressursen.'


class UserHasNoCompany(MyBaseException):
    status_code = 401
    defcon_level = DefconLevel.info
    message = 'Du er ikke registrert på et firma enda. Dette krever en invitasjon.'


class DuplicateCompany(MyBaseException):
    status_code = 403
    defcon_level = DefconLevel.warning
    message = (
        'Firmaet finnes allerede i vår database. Om dette er ditt firma, '
        'kan du prøve å snakke med en kollega om å få en invitasjonsnøkkel. '
        'Du kan også kontakte oss, om du mener noen utenom deres firma har '
        'registrert seg som dere uten samtykke.')


class NotACustomer(MyBaseException):
    message='Fant ingen kunde.'
    defcon_level=DefconLevel.default
    status_code=403


class NotARoom(MyBaseException):
    message='Fant ikke dette rommet i databasen.'
    defcon_level=DefconLevel.default
    status_code=403


class NotAProduct(MyBaseException):
    message='Fant ikke dette produktet i databasen.'
    defcon_level=DefconLevel.default
    status_code=403
