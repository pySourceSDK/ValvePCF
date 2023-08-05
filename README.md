[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/pySourceSDK/ValvePCF/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/valvepcf.svg)](https://pypi.python.org/pypi/valvepcf/)
[![Platforms](https://img.shields.io/badge/platform-Linux,_MacOS,_Windows-blue)]()
[![PyPI version fury.io](https://badge.fury.io/py/valvepcf.svg)](https://pypi.python.org/pypi/valvepcf/)
[![GitHub Workflow Status (with event)](https://github.com/pySourceSDK/ValvePCF/actions/workflows/CI.yml/badge.svg)]()
[![Test coverage](https://github.com/pySourceSDK/ValvePCF/blob/master/docs/source/coverage.svg "coverage")]()

# ValvePCF

ValvePCF is a Python library designed to parse and edit .PCF files, which are utilized for storing particle effects data in Valve's Source engine.

Full documentation: https://pysourcesdk.github.io/ValvePCF/

## Installation

### PyPI

ValvePCF is available on the Python Package Index. This makes installing it with pip as easy as:

```bash
pip3 install valvepcf
```

### Git

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

```bash
git clone git@github.com:pySourceSDK/ValvePCF.git
```

and install it with:

```bash
python3 setup.py install
```

## Usage

Here's a few example usage of ValvePCF

### Parsing

Parsing can be done by creating an instance of Pcf with a path.

```python
>>> from valvepcf import Pcf
>>> pcf = Pcf('C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/particles/custom.pcf')
```
