# outpostcli

Produce a bill of materials for an outpost construction.

## Operation

Prepare a definition of the components of your outpost in YAML (it's a very simple format, just a bulleted list using hypens as a bullet):

```
- Landing Pad - Small
- Industrial Workbench
- 3 Wind Turbine - Advanced (25 power)
- Extractor - Copper
- 1 Storage - Solid - Large (copper)
- Extractor - Fluorine
- 1 Storage - Gas - Large (fluorine)
- Extractor - Ionic Liquid
- 1 Storage - Liquid - Large (ionic liquid)
```

Now run the bill of materials generator to process that list and the BOM will be returned:

```
$ outpost bom procyon-iii.yml
- Adaptive Frame: 30
- Aluminum: 77
- Copper: 23
- Iron: 51
- Isocentered Magnet: 6
- Nickel: 24
- Tungsten: 18
```

## Project Features

* [outpostcli](http://OutpostCLI.readthedocs.io/)
* a starter [Click](http://click.pocoo.org/5/) command-line application
* automated unit tests you can run with [pytest](https://docs.pytest.org/en/latest/)
* a [Sphinx](http://www.sphinx-doc.org/en/master/) documentation project

## Getting Started

The project's documentation contains a section to help you
[get started](https://OutpostCLI.readthedocs.io/en/latest/getting_started.html) as a developer or user of the library.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://OutpostCLI.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **Alex Satrapa** - *Initial work* - [github](https://github.com/AlexSatrapa)

See also the list of [contributors](https://github.com/AlexSatrapa/outpostcli/contributors) who participated in this project.

## License

Copyright (c) Alex Satrapa

All rights reserved.