# Contributing to Cisco Network Topology Simulator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Update documentation
7. Commit with clear messages
8. Push to your fork
9. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cisco-network-topology-simulator.git
cd cisco-network-topology-simulator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
black .
flake8 .
```

### Coding Standards

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Write unit tests for new features
- Keep functions focused and small
- Comment complex logic

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add security audit feature for network topology

- Implement vulnerability scanning
- Add compliance checking for PCI-DSS
- Include CVE database integration

Fixes #123
```

## Testing

- Write unit tests for all new code
- Ensure test coverage remains above 80%
- Test on multiple Python versions (3.9, 3.10, 3.11)
- Include integration tests for major features

## Documentation

- Update README.md for new features
- Add docstrings to all public functions
- Include code examples
- Update API documentation

## Questions?

Feel free to open an issue for any questions or reach out to:
- Email: mangesh.bhattacharya@ontariotechu.net
- GitHub: @Mangesh-Bhattacharya

Thank you for contributing! 🎉
