# GVALUATOR

Stock valuation bot that pull in various financial info for a given asset and updates a Google Sheet for stock valuation (gvaluator).

----
## Installation

The following steps are for one-time only setup to install & run the program.

Create new virtual environment inside the working directory

```
python3 -m venv env
```

Activate the environment

```
source env/bin/activate
```

Install libraries

```
pip3 install -r requirements.txt
```

Testing
All unit tests can be found in ./tests/ and are [pytest](https://docs.pytest.org/en/latest/)
```
pytest
```

Linting
```
flake8 gvaluator.py
```

Isort
For import module sorting
```
isort gvaluator.py
```

Black
Code formatting
```
black gvaluator.py
```

Git Hook
Install pre-commit hook
```
pre-commit install
```

----

## Usage
The following will configure the environment, execute the program and deactivate accordingly.


Activate the virtual environment
```
source env/bin/activate
```

Execute Script
```
TBD
```

Deactivate the environment
```
deactivate
```
