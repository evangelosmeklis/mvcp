# Contributing to MVCP

Thank you for your interest in contributing to MVCP (Model Version Control Protocol)! We appreciate any help, whether it's fixing bugs, adding features, improving documentation, or suggesting ideas.

## Getting Started

### Prerequisites

- Git
- Python 3.8 or higher
- A GitHub account

### Development Setup

1. **Fork the Repository**
   
   Start by forking the repository to your own GitHub account by clicking the "Fork" button at the top right of the [MVCP repository](https://github.com/evangelosmeklis/mvcp).

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/mvcp.git
   cd mvcp
   ```

3. **Set Up a Development Environment**

   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

4. **Create a Branch**

   Create a branch for your work:

   ```bash
   git checkout -b feature/your-feature-name
   ```

   Use a descriptive branch name that reflects what you're working on:
   - `feature/...` for new features
   - `fix/...` for bug fixes
   - `docs/...` for documentation changes
   - `refactor/...` for code refactoring

## Contribution Process

### 1. Find or Create an Issue

- Check existing [issues](https://github.com/evangelosmeklis/mvcp/issues) to see if your idea or bug report already exists
- If it doesn't exist, create a new issue describing what you'd like to work on
- Wait for maintainer feedback before proceeding with major changes

### 2. Make Your Changes

- Follow the coding style and guidelines used in the project
- Keep your changes focused and limited to the issue you're addressing
- Add or update tests for your changes
- Update documentation as needed

### 3. Test Your Changes

- Run the existing tests to ensure you haven't broken anything:
  ```bash
  pytest
  ```

- Add new tests for your functionality

### 4. Commit Your Changes

- Use clear, concise commit messages
- Reference the issue number in your commit message:
  ```
  feat: add new option for checkpoint naming (#42)
  ```

- Follow [conventional commits](https://www.conventionalcommits.org/) for commit messages:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `test:` for test changes
  - `refactor:` for code refactoring
  - `style:` for formatting changes
  - `chore:` for general maintenance tasks

### 5. Submit a Pull Request

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to the [MVCP repository](https://github.com/evangelosmeklis/mvcp) and create a pull request
3. Describe your changes in detail, referencing any related issues
4. Wait for a review from the maintainers

## Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Keep line length to a maximum of 88 characters (compatible with Black formatter)
- Use docstrings for all modules, classes, and functions

### Testing

- Add tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for high test coverage

### Documentation

- Update the README.md if necessary
- Add docstrings to any new functions, classes, or modules
- Update any affected documentation in the docs directory

## Pull Request Review Process

1. Maintainers will review your PR as soon as possible
2. They might request changes or ask questions
3. Address any feedback and push changes to the same branch
4. Once approved, a maintainer will merge your PR

## License

By contributing to MVCP, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have any questions or need help, don't hesitate to:

- Open an issue with your question
- Reach out to the maintainers

Thank you for contributing to MVCP! 