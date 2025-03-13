Development
==========

This section covers development processes and standards for ``bluetermgen``.

Continuous Integration and Deployment
-----------------------------------

``bluetermgen`` uses GitHub Actions for continuous integration and deployment:

Testing
~~~~~~~

All code changes are automatically tested on:

* Multiple Python versions: 3.8, 3.9, 3.10, and 3.11
* Multiple operating systems: Ubuntu, Windows, and macOS

Documentation
~~~~~~~~~~~~

Documentation is automatically built using Sphinx when changes are made to:

* Any Python file in the ``bluetermgen`` package
* Any documentation files in the ``docs`` directory

The documentation is hosted on Read the Docs at `<https://bluetermgen.readthedocs.io>`_.

Publishing
~~~~~~~~~

When a new release is created on GitHub, the package is automatically:

1. Built using ``build``
2. Checked with ``twine check``
3. Uploaded to PyPI

Release Process
-------------

To release a new version:

1. Update the version number in ``pyproject.toml``
2. Update the ``CHANGELOG.rst`` with details of changes
3. Commit these changes
4. Create a new release on GitHub with an appropriate tag (e.g., ``v0.1.0``)
5. The GitHub Actions workflow will automatically publish to PyPI