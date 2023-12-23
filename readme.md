# MMpy Tools

Collection of tools I used reapatedly in Python (but they do not deserve a stand-alone repo :)

## Classes

* **MySQL**: Custom MySQL connector

## Installation

### Create python virtual environment

#### Linux

```bash
python3 -m venv env
source env/Scripts/activate
```

#### Windows

```bash
python -m venv env
source env/Scripts/activate
```


## Dependencies:

Will be done by default if installed from pypi, otherwise run

```bash
# install including dependencies for building docs etc.
pip install -r requirements.txt

# OR only package
pip install -e .

# OR directly from github
pip install -e git+https://github.com/emenems/mmpy-tools.git#egg=mmpy_tools
```


## Test

* To carry out [unit-test](https://docs.pytest.org/en/latest/), just go to the root folder (where setup.py is located) and run `pytest` from shell

## Usage

```python
from mmpy_tools import MySQL

# In case the ENV valriables are stored in .env file:
from dotenv import load_dotenv
load_dotenv()

help(MySQL)
```
