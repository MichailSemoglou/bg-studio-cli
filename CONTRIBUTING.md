# Contributing to BG Studio CLI

## Prerequisites

- Python 3.8+
- Git
- Virtual environment

## Development Setup

```bash
git clone https://github.com/MichailSemoglou/bg-studio-cli.git
cd bg-studio-cli
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Bug Reports

Include:

- Reproduction steps
- Expected vs actual behavior
- Environment details
- Error messages

## Feature Requests

- Description and use case
- Implementation approach
- Examples/mockups

## Pull Request Process

```bash
git checkout -b feature/name
# Make changes, add tests, update docs
python bgstudio.py --help  # Test
git commit -m "feat: description"
git push origin feature/name
```

## Code Standards

- PEP 8 (100 char lines)
- Double quotes for strings
- Grouped imports
- Docstrings for functions

## Commit Format

`<type>: <description>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Testing

```bash
pytest
pytest --cov=bgstudio
pytest tests/test_cli.py
```

Tests in `tests/` directory, named `test_*.py`

## Documentation

- Public functions need docstrings
- Google-style docstrings
- Type hints
- Update README for new features

## License

Contributions licensed under MIT License.
