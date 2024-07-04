<!--
SPDX-FileCopyrightText: 2024 Benedikt Franke <benedikt.franke@dlr.de>
SPDX-FileCopyrightText: 2024 Florian Heinrich <florian.heinrich@dlr.de>

SPDX-License-Identifier: Apache-2.0
-->

# Federated Learning Client Base Image

This repository provides a small client base package including client server communication helpers.
This package should simplify the Federated Learning platform client development in Python.

This project is a component of the Federated Learning (FL) platform, serving as a proof of concept for the [Catena-X](https://catena-x.net/en) project.
The FL platform aims to demonstrate the potential of federated learning in a practical, real-world context.

For a comprehensive understanding of the FL platform, please refer to the official [FL platform documentation](https://dlr-ki.github.io/fl-documentation).

A complete list of all repositories relevant to the FL platform can be found [here](https://dlr-ki.github.io/fl-documentation#repositories).

## Get Started

This README.md is primarily intended for developers and contributors, providing necessary information for setup, installation, and contribution guidelines.
If you're interested in using or testing this project, we recommend starting with the [GitHub pages](https://dlr-ki.github.io/fl-demonstrator-client).
They offer a more user-friendly interface and comprehensive guides to get you started.

An example of how this package can be used is the [MNIST example client](https://github.com/DLR-KI/fl-demonstrator-mnist) implementation.

## Requirements

- python 3.7 or later  
  `which python`
- virtualenv or venv  
  `pip install -U virtualenv`

## Install

```bash
# create virtual environment
virtualenv -p $(which python3.7) .venv
# or
# python -m venv .venv

# activate our virtual environment
source .venv/bin/activate

# update pip (optional)
python -m pip install -U pip

# install
./dev install -U -e ".[all]"
```

## Helpers

```txt
$ ./dev --help
usage: ./dev <action> [options]

positional arguments:
  {clean,coverage,coverage-report,doc,doc-build,docker-build,help,install,licenses,licenses-check,lint,lint-code,lint-doc,lint-scripts,mypy,safety-check,start,test,version,versions}
                        Available sub commands
    help                Show this help message and exit
    start               Run the application
    docker-build        Build docker images for local development
    test                Run all tests
    lint                Run all linter
    lint-code           Run code linter
    lint-doc            Run documentation linter
    lint-scripts        Run bash script linter
    mypy                Run type checker
    coverage            Run unit tests
    coverage-report     Generate test coverage report
    doc                 Start documentation server
    doc-build           Build documentation
    licenses            Generate licenses
    licenses-check      Check licenses
    safety-check        Check dependencies for known security vulnerabilities
    install             Install package
    clean               Clean up local files
    version             Show package version
    versions            Show versions

options:
  --no-http-serve       Do not serve the action result via HTTP
```

## Contribution

- Type-Save and linting with mypy+flake8
- Scripts and examples for linux, wsl (bash)

### Documentation

This projects is using the Docstring style from
[Google](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
At least public classes, methods, fields, ... should be documented.

```python
"""
This is the single line short description.

This is the multiline or long description.
Note, that the whole Docstring support markdown styling.

The long description can also contains multiple paragraphs.

Args:
    log_filepath (str): Log file path.
    ensure_log_dir (bool, optional): Create directory for the log file if not exists. Defaults to True.

Returns:
    Dict[str, Any]: logging configuration dict
"""
```

## Credits

<div>
    <div style="display: inline-block; width: 42%;">
        <img src="./docs/assets/logo/DLR_Logo_EN_black.svg#gh-light-mode-only" alt="DLR" style="width: 100%;" />
        <img src="./docs/assets/logo/DLR_Logo_EN_white.svg#gh-dark-mode-only" alt="DLR" style="width: 100%" />
        <div style="text-align: center;">
            <img src="./docs/assets/logo/catena-x-black.svg#gh-light-mode-only" alt="Catena-X" style="width: 80%;" />
            <img src="./docs/assets/logo/catena-x-white.svg#gh-dark-mode-only" alt="Catena-X" style="width: 80%;" />
        </div>
    </div>
    <div style="display: inline-block; width: 55%; float: right;">
        <img src="./docs/assets/logo/EN_fundedbyEU_VERTICAL_RGB_POS.svg#gh-light-mode-only" alt="European Union" style="width: 44%;" />
        <img src="./docs/assets/logo/EN_fundedbyEU_VERTICAL_RGB_NEG.svg#gh-dark-mode-only" alt="European Union" style="width: 44%;" />
        <img src="./docs/assets/logo/bmwk_en.png" alt="BMWK" style="width: 44%; float: right;" />
    </div>
</div>
