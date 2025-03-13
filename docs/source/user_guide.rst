User Guide
=========

This guide provides detailed information about each component in the ``bluetermgen`` library.

Messages
-------

The ``Message`` class creates bordered text boxes with various styling options.

.. code-block:: python

   from bluetermgen import Message

Basic Usage:

.. code-block:: python

   # Simple message
   msg = Message("Hello World")
   
   # Message with styling
   msg = Message("Warning!", style="bold")
   
   # Centered message with minimum width
   msg = Message("Important", align="center", min_width=20)

**Message Parameters**

* ``message_text`` (str or list): The message content.
* ``align`` (str): Text alignment - "left" (default), "center", or "right".
* ``min_width`` (int): Minimum width of the message box.
* ``style`` (str): Border style - "single" (default), "double", "bold", or "simple".
* ``padx`` (int or tuple): Horizontal padding, either uniform (int) or custom (left, right).

Menus
-----

The ``Menu`` class creates interactive menus with optional headers, footers, and indexing.

.. code-block:: python

   from bluetermgen import Menu

Basic Usage:

.. code-block:: python

   # Basic menu
   menu = Menu(["Option 1", "Option 2", "Option 3"])
   
   # Menu with header and footer
   menu = Menu(
       menu_items=["Option 1", "Option 2", "Option 3"],
       header="Main Menu",
       footer="Select an option:"
   )
   
   # Menu with numbering
   menu = Menu(
       menu_items=["Option 1", "Option 2", "Option 3"],
       index="number.dot"  # Results in "1.", "2.", "3."
   )

**Menu Parameters**

* ``menu_items`` (list): List of menu options.
* ``header`` (str or list, optional): Menu header text.
* ``footer`` (str or list, optional): Menu footer text.
* ``index`` (str, optional): Indexing style for menu items.
* ``custom_index_prefix`` (list, optional): Custom prefixes for menu items.
* ``align`` (tuple): Alignment for (header, items, footer) - "left", "center", or "right".
* ``min_width`` (int): Minimum width of the menu.
* ``style`` (str): Border style - "single", "double", "bold", or "simple".
* ``padx`` (int or tuple): Horizontal padding configuration.

**Indexing Options**

* ``"number.dot"``: "1.", "2.", "3."
* ``"number.parentheses"``: "1)", "2)", "3)"
* ``"letter.upper.dot"``: "A.", "B.", "C."
* ``"letter.upper.parentheses"``: "A)", "B)", "C)"
* ``"letter.lower.dot"``: "a.", "b.", "c."
* ``"letter.lower.parentheses"``: "a)", "b)", "c)"

Tables
-----

The ``Table`` class displays data in a formatted table with optional headers and styling.

.. code-block:: python

   from bluetermgen import Table

Basic Usage:

.. code-block:: python

   # Table from list of lists
   data = [
       ["Header 1", "Header 2"],
       ["Row 1 Col 1", "Row 1 Col 2"],
       ["Row 2 Col 1", "Row 2 Col 2"]
   ]
   table = Table(data)
   
   # Table from dictionaries
   data = [
       {"Name": "John", "Age": "25"},
       {"Name": "Alice", "Age": "30"}
   ]
   table = Table(data)
   
   # Table with custom alignment and row separators
   table = Table(
       data,
       align=("center", "right"),  # Center headers, right-align data
       row_sep=True  # Add separators between rows
   )

**Table Parameters**

* ``table_data`` (list): Data as list of lists or list of dictionaries.
* ``headers`` (list or str, optional): Table header configuration.
* ``index`` (bool): Whether to show row numbers.
* ``align`` (tuple): Alignment for (header, data).
* ``custom_align`` (dict): Custom alignment per column.
* ``min_width`` (int or dict): Minimum column widths.
* ``style`` (str): Border style.
* ``padx`` (int or tuple): Horizontal padding.
* ``row_sep`` (bool): Whether to show separators between rows.