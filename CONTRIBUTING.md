# Contributing Guidelines for RAGGENIE

## 🪜 Steps to Contribute

To make a contribution, follow the following steps:

1. Fork and clone this repository
2. Do the changes on your fork
3. If you modified the code (new feature or bug-fix), please add tests for it
4. Check the linting [see below](https://github.com/sirocco-ventures/raggenie/blob/main/CONTRIBUTING.md#-Linting)
5. Ensure that all tests pass [see below](https://github.com/sirocco-ventures/raggenie/blob/main/CONTRIBUTING.md#-Testing)
6. Submit a pull request

For more details about pull requests, please read [GitHub's guides](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## 📦 Package manager

At the moment we are using pip as our package manager. Please make sure to include all the required libraries in `requirements.txt` at the time of build.

## 📌 Pre-commit

To ensure our standards, make sure to install pre-commit before starting to contribute.

```bash
pre-commit install
```

## 🧹 Linting
We use `Flake8` for linting our code. You can use the linter by running the following code.
```bash
make linting
```

## 📝 Code formatting
We use `Flake8` as our code formatter. You can format the code using the following code.
```bash
make formatting
```

## 🗒 Spellcheck
We use `codespell` for spell checking our code. For running the spellchecker run the following code.
```bash
make spellcheck
```

## 🧪 Testing
we use `pytest` for integration testing the RAGGENIE. and `unittest` for unit testing individual components.
for unit testing run the following code
```bash
make unit-test
```

for integration testing run the following code
```bash
make integration-test
```
