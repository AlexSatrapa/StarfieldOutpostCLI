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
        self.power_check: bool = True


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@click.option('--power-check', is_flag=True)
@pass_info
def outpost(info: Info, verbose: int, power_check=False):
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
    info.power_check = power_check

@outpost.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))

@outpost.command()
@click.argument('yaml_specification', type=click.File('rb'), required=False)
@click.option('--power-check', is_flag=True)
def normalise(yaml_specification, power_check=False):
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
    if power_check:
        power_result = materials.power_check(yaml_structure)
        click.echo(F'Power check: {power_result}')
