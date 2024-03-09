# outpostcli

Produce a bill of materials for an outpost construction.

## Operation

WIP: Prepare a definition of the components of your outpost in YAML-ish Markdown format (it's a very simple format, just a bulleted list using hypens as a bullet):

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

WIP stretch goal: coalesce common elements:

```
$ outpost normalise
[manually paste in the following]
- Landing Pad - Small
- Industrial Workbench
- 3 Wind Turbine - Advanced (25 power)
- Extractor - Copper
- Storage - Solid - Large (copper)
- Extractor - Beryllium
- Storage - Solid - Large (beryllium)
[calculator returns the following]
- Landing Pad - Small
- Industrial Workbench
- 3 Wind Turbine - Advanced (25 power)
- 2 Extractor (beryllium, copper)
- 2 Storage - Solid - Large (beryllium, copper)
```

## Project Features

* a starter [Click](http://click.pocoo.org/5/) command-line application
* automated unit tests you can run with [pytest](https://docs.pytest.org/en/latest/)
* on macOS check out the "make redgreen" option which runs the test suite any time you save a change

## Getting Started

* Clone the Project: `git clone git@github.com:AlexSatrapa/StarfieldOutpostCLI.git`
* run `make dev-env`

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

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
