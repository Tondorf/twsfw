[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Documentation](https://github.com/tondorf/twsfw/actions/workflows/deploy_docs.yml/badge.svg)](https://tondorf.github.io/twsfw/)
[![Test coverage](https://codecov.io/gh/tondorf/twsfw/graph/badge.svg?token=Q0WZP462YA)](https://codecov.io/gh/tondorf/twsfw)
[![Unit tests](https://github.com/tondorf/twsfw/actions/workflows/run_tests.yml/badge.svg)](https://codecov.io/gh/tondorf/twsfw)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# twsfw

<!-- add description here -->

## Documentation

Find the documentation [here](https://tondorf.github.io/twsfw).

## Installation

Checkout latest version from [GitHub](https://github.com/Tondorf/twsfw) including the submodules:

```bash
$ git clone --recurse-submodules git@github.com:Tondorf/twsfw.git
```

Then, install the Python package:

```bash
# production installation
$ pip install -r requirements.txt
$ pip install -e .

# development installation
$ pip install -e .[dev]
$ pre-commit install
```

## Usage

```python
import twsfw
twsfw.__version__
```

## Run unit tests

```bash
$ pytest --cov=twsfw
```

## Generate documentation

```bash
$ cd docs && make html
[...]
The HTML pages are in build/html.
```
