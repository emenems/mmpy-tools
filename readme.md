# MMpy Tools

Collection of tools I used reapatedly in Python (but they do not deserver a stand-alone repo :)

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
```


## Test

* To carry out [unit-test](https://docs.pytest.org/en/latest/), just go to the root folder (where setup.py is located) and run `pytest` from shell

## Usage

```python
from chatbot_tools import MySQL
help(MySQL)
```
