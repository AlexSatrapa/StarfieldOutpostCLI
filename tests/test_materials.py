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
            'label_text': None,
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
            'label_text': None,
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
            'label_text': None,
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
        self.assertEqual( expanded, expected )

    def test_condenses_detail_to_show_only_spec(self):
        expanded = [
        {
            'name': 'Wind Turbine - Advanced',
            'count': 2,
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

class DescribeItemNameMatchingRegex(unittest.TestCase):
    def test_matches_undecorated_item_name(self):
        item_name = 'Wind Turbine - Advanced'
        match_result = materials.item_name_regex.fullmatch(item_name)
        self.assertEqual(match_result['item_name'], item_name)

    def test_matches_item_name_with_number_in_front(self):
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

    def test_matches_item_name_with_power_label(self):
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

    def test_matches_item_name_with_count_and_labels(self):
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
