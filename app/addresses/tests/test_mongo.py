# -*- coding: utf-8 -*-
"""Unit-tests for adresses."""
# import os
import unittest

import address_pymongo as address

known_values_postareas = {
    'Kristiansand S': [
        4632, 4612, 4628, 4629, 4630, 4634, 4622, 4631, 4618, 4617, 4626, 4613,
        4635, 4621, 4636, 4615, 4624, 4610, 4638, 4620, 4614, 4616, 4637, 4639, 4623,
        4611, 4633, 4608,
    ]}

known_values_post_codes = {
    4633: 'Kristiansand S',
    8250: 'Rognan'
}

known_values_street_name = {
    'Kongens gate': [
        {'post_code': 1606, 'post_area': 'FREDRIKSTAD'},
        {'post_code': 1530, 'post_area': 'MOSS'},
        {'post_code': 1809, 'post_area': 'ASKIM'},
        {'post_code': 153, 'post_area': 'OSLO'},
        {'post_code': 3510, 'post_area': 'HØNEFOSS'},
        {'post_code': 3611, 'post_area': 'KONGSBERG'},
        {'post_code': 3210, 'post_area': 'SANDEFJORD'},
        {'post_code': 3211, 'post_area': 'SANDEFJORD'},
        {'post_code': 3717, 'post_area': 'SKIEN'},
        {'post_code': 4610, 'post_area': 'KRISTIANSAND S'},
        {'post_code': 4608, 'post_area': 'KRISTIANSAND S'},
        {'post_code': 6002, 'post_area': 'ÅLESUND'},
        {'post_code': 7011, 'post_area': 'TRONDHEIM'},
        {'post_code': 7013, 'post_area': 'TRONDHEIM'},
        {'post_code': 7012, 'post_area': 'TRONDHEIM'},
        {'post_code': 7715, 'post_area': 'STEINKJER'},
        {'post_code': 7713, 'post_area': 'STEINKJER'},
        {'post_code': 8006, 'post_area': 'BODØ'},
        {'post_code': 8514, 'post_area': 'NARVIK'},
        {'post_code': 9950, 'post_area': 'VARDØ'},
        {'post_code': 9900, 'post_area': 'KIRKENES'}],
    'Bergtoras vei': [{'post_code': 4633, 'post_area': 'KRISTIANSAND S'}],
    'Justnesveien': [{'post_code': 4634, 'post_area': 'KRISTIANSAND S'}]
    }



class AddressKnownValuesTests(unittest.TestCase):
    """Test lookup of adresses in db."""

    def test_get_post_code(self):
        """Test getting post_code for a postal area."""
        for key, value in known_values_postareas.items():
            result = address.get_post_code_for_post_area(key)
            self.assertCountEqual(result, value)

    def test_get_post_area_for_post_code(self):
        """Test getting post_area for a post-code"""
        for key, value in known_values_post_codes.items():
            area = address.get_post_area_for_post_code(key)
            self.assertEqual(area.lower(), value.lower())

    def test_get_address_from_street_name(self):
        """Test against known values for street_names"""
        for key, value in known_values_street_name.items():
            results = address.get_address_from_street_name(key, limit=1000)
            parsed_result = []
            for result in results:
                self.maxDiff=None
                parsed_result.append({
                    'post_code': result["post_code"],
                    'post_area': result["post_area"]
                })
            self.assertCountEqual(parsed_result, value)


if __name__ == '__main__':
    unittest.main()
