[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/pySourceSDK/ValveFGD/blob/master/LICENSE.txt)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/valvefgd.svg)](https://pypi.python.org/pypi/valvefgd/)
[![PyPI version fury.io](https://badge.fury.io/py/valvefgd.svg)](https://pypi.python.org/pypi/valvefgd/)
[![alt text](https://github.com/pySourceSDK/ValveFGD/blob/master/docs/source/coverage.svg "coverage")]()

# ValvePCF

ValvePCF is a Python library for parsing .pcf files for the Source Engine. It provides ways to read, modify and write pcf files.

Full documentation: https://pysourcesdk.github.io/ValveFGD/

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

Here's a few example usage of valvePcf

### Parsing

Parsing can be done by creating an instance of Pcf with a path.

```python
>>> from valvepcf import Pcf
>>> pcf = Pcf('C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/tf/particles/custom.pcf'
```