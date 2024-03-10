"""
Provides an interface to the Starfield materials database.

.. currentmodule:: outpostcli.materials
.. moduleauthor:: Alex Satrapa <grail@goldweb.com.au>
"""

import os
import re
import click
import yaml

materials_content = None # pylint: disable=C0103
materials_dict = {}      # pylint: disable=C0103
item_name_regex = re.compile(
    r'^(?P<item_count>\d+)?\s*(?P<item_name>\w+[^(]*?)\s*(?P<labels>\(.+\)\s*$)?'
)
power_override_regex = re.compile(
    r'((?P<override_prefix>\d+)\s+power|power:\s*(?P<override_suffix>\d+))',
    flags=re.IGNORECASE
)

def load_materials(yamlpath):
    """
    Load the materials database YAML from the given path.
    """
    with open(yamlpath, 'r', encoding='utf8') as yaml_source:
        materials_content = yaml.safe_load(yaml_source) # pylint: disable=W0621
        for materials_entry in materials_content:
            materials_dict[materials_entry['name']] = materials_entry

def load_default():
    """
    Load the materials database from the default path which is the
    materials.yml file located beside this module.
    """
    if materials_content is None:
        filepath = os.path.realpath(__file__)
        dirpath = os.path.dirname(filepath)
        yamlpath = F'{dirpath}/materials.yml'
        if os.path.exists(yamlpath):
            load_materials(yamlpath)
        else:
            raise FileNotFoundError(F'Could not find {yamlpath}')

def expand(yaml_string):
    """
    Given a YAML description of the components of an outpost, return a list of the
    materials DB entries for those items.
    """
    yaml_structure = yaml.safe_load(yaml_string)
    expanded_structure = []
    for item in yaml_structure:
        if isinstance(item, dict):
            item_text = next(iter(item.keys()))
            item_count = int(item[item_text])
        else:
            item_text = item
            item_count = 1
        match_result = item_name_regex.fullmatch(item_text)
        if match_result is None:
            click.echo(F'{item_text} could not be resolved to an item name', err=True)
        else:
            item_name = match_result['item_name']
            if match_result['item_count'] is not None:
                item_count = int(match_result['item_count'])
            if match_result['labels'] is not None:
                label_text = match_result['labels']
            else:
                label_text = ''
        if item_name not in materials_dict:
            click.echo(F'{item_name} was not found in materials database', err=True)
            continue

        item_details = materials_dict[item_name]
        item_details['count'] = item_count
        item_details['label_text'] = label_text
        power_override_value = power_override(label_text)
        if power_override_value is not None and 'structure' in item_details:
            item_details['structure']['power'] = power_override_value
        expanded_structure.append(item_details)
    return expanded_structure

def condense(yaml_structure):
    """
    Given a data structure, produce a normalised YAML outpost specification.
    """
    normalised_structure = []
    for entry in yaml_structure:
        if entry['count'] > 1:
            normalised_entry = {
                entry['name']: entry['count']
            }
        else:
            normalised_entry = entry['name']
        normalised_structure.append(normalised_entry)
    yaml_text = yaml.dump(normalised_structure)
    return yaml_text

def power_override(label_string) -> int:
    """
    Given a string, determine if it contains a power override.

    Power override is presented as the word 'power' accompanied by an integer:

    - Solar Dome (power: 3)
    - Solar Dome (3 power)

    A power override is an observed power output for a solar or wind power source.
    These power sources have variable output depending on the world they're deployed
    on. Solar will tend to get weaker further from the star, wind will get weaker with
    less atmosphere.
    """
    match_result = power_override_regex.search(label_string)
    override_value = None
    if match_result is not None:
        if match_result['override_prefix'] is not None:
            override_value = int(match_result['override_prefix'])
        if match_result['override_suffix'] is not None:
            override_value = int(match_result['override_suffix'])
    return override_value
