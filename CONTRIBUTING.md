# Contributing to YouTube Scam Ad Scanner

Thank you for your interest in contributing to this project! This guide will help you get started.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/youtube-scam-ad-scanner.git
   cd youtube-scam-ad-scanner
   ```

3. **Set up your development environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   
   pip install -r requirements.txt
   ```

4. **Create a branch for your changes:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Adding New Features

#### Adding Scam Indicators

1. Add keywords/patterns to `src/scanner.py` in the `ScamIndicators` class:
   ```python
   class ScamIndicators:
       NEW_INDICATOR_TYPE = [
           'pattern1',
           'pattern2',
       ]
   ```

2. Implement detection logic in `ScamScanner` class:
   ```python
   def _analyze_new_indicator(self, content: str) -> Tuple[int, List[str]]:
       score = 0
       indicators = []
       # Detection logic here
       return score, indicators
   ```

3. Add tests in `tests/test_scanner.py`:
   ```python
   def test_new_indicator_detection(self, scanner):
       """Test detection of new indicator"""
       # Test implementation
   ```

#### Adjusting Risk Scores

- Update scoring values in `src/config.py`
- Document the reasoning for score changes
- Ensure tests still pass with new scores

### Testing

**Always add tests for new features:**

```bash
# Run tests before committing
pytest

# Check test coverage
pytest --cov=src --cov-report=term-missing

# Run specific tests
pytest tests/test_scanner.py::TestClassName::test_method_name
```

**Test Guidelines:**
- Aim for >80% code coverage
- Write both unit tests and integration tests
- Use descriptive test names
- Test edge cases and error conditions
- Mark slow tests with `@pytest.mark.slow`

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

**Examples:**
```
feat(scanner): add detection for cryptocurrency scams

fix(scanner): correct regex pattern for domain validation

docs(readme): update installation instructions

test(scanner): add tests for URL redirect detection
```

## Pull Request Process

1. **Update documentation** if needed (README, EXAMPLES, etc.)
2. **Add tests** for new functionality
3. **Ensure all tests pass:** `pytest`
4. **Update CHANGELOG** (if present) with your changes
5. **Create a pull request** with a clear description:
   - What changes were made
   - Why the changes are needed
   - How to test the changes
   - Any potential side effects

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented if necessary)
```

## Areas for Contribution

### High Priority

1. **Machine Learning Integration**
   - Implement ML models for scam detection
   - Create training data pipeline
   - Add feature extraction for ML

2. **Browser Extension**
   - Chrome/Firefox extension to capture YouTube ads
   - Automatic URL extraction from ads
   - Integration with scanner backend

3. **Selenium Integration**
   - Automated browser for JavaScript-heavy pages
   - Screenshot capture
   - Dynamic content analysis

4. **Database of Known Scams**
   - Domain blacklist/whitelist
   - Pattern database
   - Community-sourced data

### Medium Priority

5. **Performance Improvements**
   - Async URL fetching
   - Caching mechanisms
   - Batch scanning optimization

6. **Additional Heuristics**
   - Visual analysis (logo detection, design patterns)
   - Language analysis (grammar, spelling)
   - Social proof checking (fake testimonials)

7. **Reporting Features**
   - Generate detailed reports
   - Export to various formats (PDF, JSON, CSV)
   - Platform integration for reporting scams

### Low Priority

8. **CLI Improvements**
   - Interactive mode
   - Progress bars for batch scanning
   - Configuration file support

9. **API Development**
   - REST API for scanner
   - Rate limiting
   - Authentication

## Code Review Process

All submissions require review. We'll look for:

- **Functionality**: Does it work as intended?
- **Tests**: Are there adequate tests?
- **Code quality**: Is it readable and maintainable?
- **Documentation**: Are changes documented?
- **Performance**: Does it impact performance?
- **Security**: Are there security implications?

## Questions or Issues?

- Open an issue for bugs or feature requests
- Use discussions for questions and ideas
- Tag issues appropriately (bug, enhancement, question, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make the internet safer for everyone. Thank you for taking the time to contribute!
