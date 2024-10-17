## Getting Started

This project includes functional, integration, and unit testing using pytest. Tests are organized into separate folders based on their type, and a conftest.py file is used to manage shared configurations and fixtures.

### Project Structure
- `functional/`: Contains functional tests (`test_*.py`).
- `integration/`: Contains integration tests (`test_*.py`).
- `unittest/`: Contains unit tests (`test_*.py`).

### Running Tests
- Run all tests: `pytest`
- To run specific tests:
  - Functional tests: `pytest functional/`
  - Integration tests: `pytest integration/`
  - Unit tests: pytest `unittest/`

### Configuration
Test configurations and database setups are defined in conftest.py. The test environment uses SQLite for isolated testing.