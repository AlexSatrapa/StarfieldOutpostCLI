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
