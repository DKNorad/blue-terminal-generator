# Add this section to your existing contributing.rst

Continuous Integration
--------------------

This project uses GitHub Actions for continuous integration:

* **Test workflow**: Runs tests and linting on multiple Python versions and operating systems
* **Documentation workflow**: Ensures documentation builds correctly
* **Publish workflow**: Automatically publishes to PyPI when a new release is created

The configuration for these workflows is in the ``.github/workflows/`` directory.

When contributing, please ensure that your changes pass all CI checks. You can view the status of
the CI workflows directly on your pull request.