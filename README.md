# Blue Terminal Generator
Easily create messages, menus or directly visualize table data into the terminal

[![Documentation Status](https://readthedocs.org/projects/bluetermgen/badge/?version=latest)](https://bluetermgen.readthedocs.io)
[![GitHub Actions Workflow Status](https://github.com/DKNorad/blue-terminal-generator/actions/workflows/test.yml/badge.svg)](https://github.com/DKNorad/blue-terminal-generator/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/bluetermgen.svg)](https://badge.fury.io/py/bluetermgen)
[![Python Version](https://img.shields.io/pypi/pyversions/bluetermgen.svg)](https://pypi.org/project/bluetermgen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to use
#### Message
```python
from bluetermgen.message import Message

message = Message("Hello World")
print(message)
```
```
┌───────────┐
│Hello World│
└───────────┘
```

#### Menu
```python
from bluetermgen.menu import Menu

menu = Menu(
    menu_items=["Option 1", "Option 2", "Option 3"],
    header="Main Menu",
    footer="0) Exit",
    index="number_parentheses"
    )
print(menu)
```
```
┌───────────┐
│Main Menu  │
├╌╌╌╌╌╌╌╌╌╌╌┤
│1) Option 1│
│2) Option 2│
│3) Option 3│
├───────────┤
│0) Exit    │
└───────────┘
```

### Table
Table data is a list of dictionaries. The keys are used for the column headers.
```python
from bluetermgen.table import Table

table = Table(
    [
        {"name": "John", "age": 25, "city": "New York",},
        {"name": "Jane", "age": 30, "city": "San Francisco",},
        {"name": "Bob", "age": 40, "city": "Los Angeles",},
        {"name": "Alice", "age": 35, "city": "Chicago",},
    ],
)
print(table)
```
```
┌─────┬───┬─────────────┐
│name │age│city         │
├╌╌╌╌╌┼─╌╌┼╌╌╌╌╌╌╌╌╌╌╌╌╌┤
│John │25 │New York     │
│Jane │30 │San Francisco│
│Bob  │40 │Los Angeles  │
│Alice│35 │Chicago      │
└─────┴───┴─────────────┘
```

Table data is a list of lists. The first list is used for the column headers. Data order is CSV like.
```python
from bluetermgen.table import Table

table = Table(
    [
        ["Header1", "Header2", "Header3"],
        ["Row1_c1", "Row1_c2", "Row1_c3"],
        ["Row2_c1", "Row2_c2", "Row2_c3"],
        ["Row3_c1", "Row3_c2", "Row3_c3"],
    ],
)
print(table)
```
```
┌───────┬───────┬───────┐
│Header1│Header2│Header3│
├╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌┤
│Row1_c1│Row1_c2│Row1_c3│
│Row2_c1│Row2_c2│Row2_c3│
│Row3_c1│Row3_c2│Row3_c3│
└───────┴───────┴───────┘
```
