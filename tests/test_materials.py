#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_materials
.. moduleauthor:: Alex Satrapa <grail@goldweb.com.au>

Describe the use and behaviour of the outpostcli.materials module.
"""

import outpostcli.materials as materials
import pytest, unittest

class DescribeMaterialsModule(unittest.TestCase):
    def setUp(self):
        materials.load_default()

    def test_contains_expected_data(self):
        materials.load_default()
        self.assertEqual(materials.materials_dict['Aluminum']['mass'], 0.5)

    def test_expands_item_to_show_materials(self):
        specification = """
        - Wind Turbine - Advanced: 2
        - Landing Pad - Small
        - Industrial Workbench
        """
        expanded = materials.expand(specification)
        expected = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 2,
            'label_text': '',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 14,
                'cargo': 0,
            },
        },
        {
            'name': 'Landing Pad - Small',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 8,
                'Iron': 20,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            }
        },
        {
            'name': 'Industrial Workbench',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 4,
                'Iron': 3,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            },
        },
        ]
        self.assertEqual(expanded, expected)

    def test_condenses_detail_to_show_only_spec(self):
        expanded = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 2,
            'label_text': '',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 14,
                'cargo': 0,
            },
        },
        {
            'name': 'Landing Pad - Small',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 8,
                'Iron': 20,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            }
        },
        {
            'name': 'Industrial Workbench',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 4,
                'Iron': 3,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            },
        },
        ]
        specification = """
- Wind Turbine - Advanced: 2
- Landing Pad - Small
- Industrial Workbench
""".strip()
        condensed = materials.condense(expanded).strip()
        self.assertEqual( condensed, specification )

    def test_allows_local_power_generation_to_be_specified_through_labels(self):
        specification = """
        - Wind Turbine - Advanced (3 power)
        """
        expanded = materials.expand(specification)
        expected = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 1,
            'label_text': '(3 power)',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 3,
                'cargo': 0,
            },
        },
        ]
        self.assertEqual(expanded, expected)

    def test_can_coalesce_multiple_elements_of_one_type_into_one_with_item_count(self):
        expanded = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 2,
            'label_text': '(6 power)',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 6,
                'cargo': 0,
            },
        },
        {
            'name': 'Wind Turbine - Advanced',
            'count': 2,
            'label_text': '(extraction)',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 14,
                'cargo': 0,
            },
        },
        {
            'name': 'Landing Pad - Small',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 8,
                'Iron': 20,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            }
        },
        ]
        expected = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 4,
            'label_text': '(6 power) (extraction)',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 6,
                'cargo': 0,
            },
        },
        {
            'name': 'Landing Pad - Small',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 8,
                'Iron': 20,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            }
        },
        ]
        coalesced = materials.coalesce(expanded)
        self.assertEqual(expected, coalesced)

class DescribeItemName(unittest.TestCase):
    def test_can_appear_on_its_own(self):
        item_name = 'Wind Turbine - Advanced'
        match_result = materials.item_name_regex.fullmatch(item_name)
        self.assertEqual(match_result['item_name'], item_name)

    def test_can_be_prefixed_with_a_count(self):
        item_text = '2 Wind Turbine - Advanced'
        expected = {
        'item_name': 'Wind Turbine - Advanced',
        'item_count': '2',
        }
        match_result = materials.item_name_regex.fullmatch(item_text)
        found = {
            'item_name': match_result['item_name'],
            'item_count': match_result['item_count'],
        }
        self.assertEqual(found, expected)

    def test_can_have_labels_suffixed(self):
        item_text = 'Wind Turbine - Advanced (12 power)'
        expected = {
            'item_name': 'Wind Turbine - Advanced',
            'labels': '(12 power)',
        }
        match_result = materials.item_name_regex.fullmatch(item_text)
        found = {
            'item_name': match_result['item_name'],
            'labels': match_result['labels'],
        }
        self.assertEqual(found, expected)

    def test_can_be_prefied_with_a_count_and_have_labels(self):
        item_text = '2 Wind Turbine - Advanced (12 power)'
        expected = {
            'item_name': 'Wind Turbine - Advanced',
            'item_count': '2',
            'labels': '(12 power)',
        }
        match_result = materials.item_name_regex.fullmatch(item_text)
        found = {
            'item_name': match_result['item_name'],
            'item_count': match_result['item_count'],
            'labels': match_result['labels'],
        }
        self.assertEqual(found, expected)

class DescribePowerOverrideLabel(unittest.TestCase):
    def test_is_none_if_label_is_not_present(self):
        label_string = ''
        override = materials.power_override(label_string)
        self.assertIsNone(override)

    def test_is_an_integer_value_if_prefix_override_is_present(self):
        label_string = '3 power'
        override = materials.power_override(label_string)
        self.assertEqual(override, 3)

    def test_is_an_integer_value_if_suffix_override_is_present(self):
        label_string = 'power: 3'
        override = materials.power_override(label_string)
        self.assertEqual(override, 3)

    def test_is_found_if_prefix_override_present_with_other_labels(self):
        label_string = '3 power for fabricators'
        override = materials.power_override(label_string)
        self.assertEqual(override, 3)

    def test_is_found_if_suffix_override_present_with_other_labels(self):
        label_string = 'vytinium tasine power:3'
        override = materials.power_override(label_string)
        self.assertEqual(override, 3)

class DescribeCoalesceOperation(unittest.TestCase):
    def test_it_returns_a_specification_with_elements_in_same_order(self):
        specification = """
        - Wind Turbine - Advanced: 2
        - Landing Pad - Small
        - Industrial Workbench
        """
        expanded = materials.expand(specification)
        coalesced = materials.coalesce(expanded)
        self.assertEqual(coalesced, expanded)

    def test_it_collates_repeated_elements_into_the_first(self):
        specification = """
        - 2 Wind Turbine - Advanced (10 power)
        - Landing Pad - Small
        - Industrial Workbench
        - Extractor - Solid (aluminum)
        - Extractor - Solid (iron)
        - Extractor - Solid (nickel)
        - Extractor - Solid (cobalt)
        - Wind Turbine - Advanced
        """
        expanded = materials.expand(specification)
        coalesced = materials.coalesce(expanded)
        expected = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 3,
            'label_text': '(10 power)',
            'materials': {
                'Aluminum': 5,
                'Isocentered Magnet': 2,
            },
            'structure': {
                'power': 10,
                'cargo': 0,
            },
        },
        {
            'name': 'Landing Pad - Small',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 8,
                'Iron': 20,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            }
        },
        {
            'name': 'Industrial Workbench',
            'count': 1,
            'label_text': '',
            'materials': {
                'Aluminum': 4,
                'Iron': 3,
            },
            'structure': {
                'cargo': 0,
                'power': 0,
            },
        },
        {
            'name': 'Extractor - Solid',
            'count': 4,
            'label_text': '(aluminum) (iron) (nickel) (cobalt)',
            'materials': {
                'Aluminum': 4,
                'Iron': 5,
                'Tungsten': 2,
            },
            'structure': {
                'power': -5,
                'cargo': 10,
            }
        },
        ]
        self.maxDiff = None
        self.assertEqual(coalesced, expected)

class DescribePowerCheck(unittest.TestCase):
    def test_returns_zero_for_outpost_with_no_power(self):
        specification = "- Landing Pad - Small"
        expanded = materials.expand(specification)
        power_result = materials.power_check(expanded)
        self.assertEqual(power_result, 0)

    def test_returns_normal_values_with_no_override(self):
        specification = """
        - Wind Turbine - Advanced: 2
        - Landing Pad - Small
        - Industrial Workbench
        """
        expanded = materials.expand(specification)
        power_result = materials.power_check(expanded)
        self.assertEqual(power_result, 28.0)

    def test_returns_overridden_values_when_overridden(self):
        specification = """
        - 2 Wind Turbine - Advanced (6 power)
        - Landing Pad - Small
        - Industrial Workbench
        """
        expanded = materials.expand(specification)
        power_result = materials.power_check(expanded)
        self.assertEqual(power_result, 12.0)
