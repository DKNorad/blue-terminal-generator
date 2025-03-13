Examples
========

This page provides practical examples for using the ``bluetermgen`` library.

Message Examples
--------------

Simple Message
~~~~~~~~~~~~

.. code-block:: python

   from bluetermgen import Message
   
   # Basic message
   msg = Message("Hello World")
   print(msg)

Output:

.. code-block:: text

   ┌───────────┐
   │Hello World│
   └───────────┘

Styled Messages
~~~~~~~~~~~~~

.. code-block:: python

   # Different styles
   styles = ["single", "double", "bold", "simple"]
   
   for style in styles:
       msg = Message(f"Style: {style}", style=style)
       print(msg)
       print()

Alignment Examples
~~~~~~~~~~~~~~~

.. code-block:: python

   # Alignment examples
   msg = Message("Left aligned (default)", min_width=30)
   print(msg)
   print()
   
   msg = Message("Centered text", align="center", min_width=30)
   print(msg)
   print()
   
   msg = Message("Right aligned", align="right", min_width=30)
   print(msg)

Menu Examples
-----------

Basic Menu
~~~~~~~~~

.. code-block:: python

   from bluetermgen import Menu
   
   # Simple menu
   options = ["New Game", "Load Game", "Settings", "Exit"]
   menu = Menu(options)
   print(menu)

Output:

.. code-block:: text

   ┌─────────┐
   │New Game │
   │Load Game│
   │Settings │
   │Exit     │
   └─────────┘

Menu with Header and Footer
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Menu with header and footer
   menu = Menu(
       menu_items=["New Game", "Load Game", "Settings", "Exit"],
       header="MAIN MENU",
       footer="Use arrow keys to navigate"
   )
   print(menu)

Menu with Numbering
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Menu with different numbering styles
   numbering_types = [
       "number.dot", 
       "number.parentheses",
       "letter.upper.dot",
       "letter.lower.parentheses"
   ]
   
   for index_type in numbering_types:
       print(f"Index type: {index_type}")
       menu = Menu(
           menu_items=["New Game", "Load Game", "Settings"],
           index=index_type
       )
       print(menu)
       print()

Table Examples
------------

Basic Table
~~~~~~~~~

.. code-block:: python

   from bluetermgen import Table
   
   # Simple table from list of lists
   data = [
       ["Name", "Age", "City"],
       ["John", "25", "New York"],
       ["Alice", "30", "Chicago"],
       ["Bob", "22", "Los Angeles"]
   ]
   
   table = Table(data)
   print(table)

Dictionary Table
~~~~~~~~~~~~~

.. code-block:: python

   # Table from dictionaries
   data = [
       {"Name": "John", "Age": "25", "City": "New York"},
       {"Name": "Alice", "Age": "30", "City": "Chicago"},
       {"Name": "Bob", "Age": "22", "City": "Los Angeles"}
   ]
   
   table = Table(data)
   print(table)

Table with Row Separators
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Table with row separators
   table = Table(data, row_sep=True)
   print(table)

Table with Custom Alignment
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Table with custom alignment
   table = Table(
       data,
       align=("center", "right")  # Center headers, right-align data
   )
   print(table)

Advanced Example: Data Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from bluetermgen import Message, Menu, Table
   
   # Create a simple dashboard with all elements
   
   # Header
   header = Message("SYSTEM DASHBOARD", style="double", align="center", min_width=60)
   print(header)
   print()
   
   # System info table
   system_data = [
       {"Component": "CPU", "Status": "Online", "Load": "45%"},
       {"Component": "Memory", "Status": "Online", "Load": "60%"},
       {"Component": "Disk", "Status": "Online", "Load": "32%"},
       {"Component": "Network", "Status": "Online", "Load": "12%"}
   ]
   
   system_table = Table(system_data, style="single")
   print(system_table)
   print()
   
   # Menu options
   menu = Menu(
       menu_items=["View Details", "System Settings", "Run Diagnostics", "Exit"],
       header="Options",
       index="number.dot",
       style="single",
       align=("center", "left", "left")
   )
   print(menu)