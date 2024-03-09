"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: outpostcli.cli
.. moduleauthor:: Alex Satrapa <grail@goldweb.com.au>
"""
import logging
import click
from outpostcli import materials
from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info:
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def outpost(info: Info, verbose: int):
    """Run outpost."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose

@outpost.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))

@outpost.command()
@click.argument('yaml_specification', type=click.File('rb'), required=False)
def normalise(yaml_specification):
    """Normalise a YAML outpost spec.

    YAML_SPECIFICATION is the filename to read the specification from.
    If this is not provided, the specification will be read from STDIN.
    """
    if yaml_specification is None:
        input_stream = click.get_text_stream('stdin')
        yaml_specification = input_stream.read()
    materials.load_default()
    yaml_structure = materials.expand(yaml_specification)
    normalised_yaml_string = materials.condense(yaml_structure)
    click.echo(normalised_yaml_string)

@outpost.command()
@click.argument('yaml_specification', type=click.File('rb'), required=False)
def bom(yaml_specification):
    """Produce a bill of materials (BOM) from an outpost spec.

    YAML_SPECIFICATION is the filename to read the specification from.
    If this is not provided, the specification will be read from STDIN.

    Output is a Markdown list of Material:Quantity entries.
    """
    if yaml_specification is None:
        input_stream = click.get_text_stream('stdin')
        yaml_specification = input_stream.read()
    materials.load_default()
    yaml_structure = materials.expand(yaml_specification)
    bom_structure = materials.bom(yaml_structure)
    bom_markdown_items = [F'- {item}: {count}' for (item, count) in bom_structure.items()]
    bom_markdown = "\n".join(bom_markdown_items)
    click.echo("Bill of Materials:")
    click.echo(bom_markdown)
