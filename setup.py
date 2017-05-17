
"""Default data for Neighborhood-map."""

manufacturors = [
    {
        'id': 1
        'name': 'Nexans',
        'description': 'its nexans',

    },
    {
        'id': 2
        'name': 'Øglænd',
        'description': 'Øglænd.',
    }
]
product_types = [
    {
        'id': 1
        'manufacturor_id': 1
        'name': 'TXLP',
    },
]
products = [
    {
        'id': 1
        'name': 'TXLP 500W 17W/M',
        'product_type_id': 1
    }
]
product_specs = [
    {
        'key': 'effekt_230V',
        'value': '200',
        'product_id': 1
    }
]
