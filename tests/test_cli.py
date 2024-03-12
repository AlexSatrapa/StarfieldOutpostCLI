#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_cli
.. moduleauthor:: Alex Satrapa <grail@goldweb.com.au>

This is the test module for the project's command-line interface (CLI)
module.
"""
import outpostcli.cli as cli
from outpostcli import __version__
from click.testing import CliRunner, Result
import pytest, unittest
from textwrap import dedent

# To learn more about testing Click applications, visit the link below.
# http://click.pocoo.org/5/testing/

class TestOutpostCommand(unittest.TestCase):
	def test_displays_library_version_when_called_with_version_option(self):
		runner: CliRunner = CliRunner()
		result: Result = runner.invoke(cli.outpost, ["version"])
		assert (
			__version__ in result.output.strip()
		), "Version number should match library version."


	def test_normalises_output_to_outpost_specification(self):
		runner: CliRunner = CliRunner()
		result: Result = runner.invoke(cli.outpost, ["normalise", "tests/sample_spec.yml"])
		assert (
			"- Landing Pad - Small" in result.output.strip()
		), "Verbose logging should be indicated in output."

	def test_produces_a_bill_of_materials(self):
		runner: CliRunner = CliRunner()
		result: Result = runner.invoke(cli.outpost, ["bom", "tests/sample_spec.yml"])
		assert ("Isocentered Magnet: 4" in result.output.strip()), "Output should contain appropriate quantity of Isocentered Magnets"

  def test_normalise_with_power_check_produces_normalised_spec_with_power_total(self):
		runner: CliRunner = CliRunner()
		result: Result = runner.invoke(cli.outpost, ["normalise", "--power-check", "tests/sample_spec.yml"])
		expected = "\n".join(dedent("""
		- Landing Pad - Small
		- Wind Turbine - Advanced: 2

		Power check: 28.0
		""").split("\n")[1:])

		self.assertEqual(result.output, expected)
