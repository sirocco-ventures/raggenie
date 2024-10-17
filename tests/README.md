## Getting Started

This project includes functional, integration, and unit testing using pytest. Tests are organized into separate folders based on their type, and a conftest.py file is used to manage shared configurations and fixtures.

### Project Structure
- `functional/`: Contains functional tests (`test_*.py`).
- `integration/`: Contains integration tests (`test_*.py`).
- `unittest/`: Contains unit tests (`test_*.py`).

## Requirements
- `pip install pytest pytest-cov`


### Running Tests
- Run all tests: `pytest`
- To run specific tests:
  - Functional tests: `pytest functional/`
  - Integration tests: `pytest integration/`
  - Unit tests: pytest `unittest/`

### Test Coverage
To measure test coverage using pytest-cov:
- Run tests with coverage: `pytest --cov=.`
- To view detailed missing line coverage in the terminal: `pytest --cov=. --cov-report=term-missing`
- To generate an HTML coverage report: `pytest --cov=. --cov-report=term-missing --cov-report=html`



### Configuration
Test configurations and database setups are defined in conftest.py. The test environment uses SQLite for isolated testing.