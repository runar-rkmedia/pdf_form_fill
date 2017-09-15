from .oegleand import Oegleand
from .nexans import Nexans

manufacturors = {
    'Nexans': Nexans,
    'Øglænd': Oegleand
}


def get_template_schema(manufacturor, *args, **kwargs):
    if manufacturor in manufacturors:
        return manufacturors[manufacturor](*args, **kwargs)
    else:
        raise KeyError('Not a valid manufacturor-name: {}'
                       .format(manufacturor))
