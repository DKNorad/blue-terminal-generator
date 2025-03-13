Quickstart
=========

This guide will help you get started with ``bluetermgen`` by introducing its core components.

Creating Message Boxes
---------------------

.. code-block:: python

   from bluetermgen import Message
   
   # Simple message
   msg = Message("Hello World")
   print(msg)
   
   # Center-aligned message with custom style
   msg = Message(
       "Important Notice",
       style="double",
       align="center",
       min_width=30
   )
   print(msg)
   
   # Multi-line message
   msg = Message(["Line 1", "Line 2", "Line 3"])
   print(msg)

Creating Menus
-------------

.. code-block:: python

   from bluetermgen import Menu
   
   # Simple menu
   menu_items = ["New Game", "Load Game", "Settings", "Exit"]
   menu = Menu(menu_items)
   print(menu)
   
   # Menu with header, footer and numbering
   menu = Menu(
       menu_items=["New Game", "Load Game", "Settings", "Exit"],
       header="Main Menu",
       footer="Select an option:",
       index="number.dot"
   )
   print(menu)

Creating Tables
-------------

.. code-block:: python

   from bluetermgen import Table
   
   # Table from list of lists
   data = [
       ["Name", "Age", "City"],
       ["John", "25", "New York"],
       ["Alice", "30", "Chicago"],
       ["Bob", "22", "Los Angeles"]
   ]
   table = Table(data)
   print(table)
   
   # Table from list of dictionaries
   data = [
       {"Name": "John", "Age": "25", "City": "New York"},
       {"Name": "Alice", "Age": "30", "City": "Chicago"},
       {"Name": "Bob", "Age": "22", "City": "Los Angeles"}
   ]
   table = Table(data)
   print(table)