# Releasing 2.1.0

## Pre-release checklist

- [x] Version `2.1.0` in `pyproject.toml` and `range_key_dict/__init__.py`
- [x] `CHANGELOG.md` updated for 2.1.0
- [x] CI green on `main` (tests 3.8–3.13, lint, coverage badge)
- [x] Local: `pytest`, `ruff check`, `ruff format --check`, `mypy`, `ty check`
- [x] `python -m build` produces sdist + wheel with only `range_key_dict/`

## Publish steps

```bash
# From a clean tree on main
python -m pip install --upgrade build twine
python -m build
twine check dist/range_key_dict_2-2.1.0*

# PyPI (use your API token)
twine upload dist/range_key_dict_2-2.1.0*

# GitHub release
git tag -a v2.1.0 -m "Release 2.1.0"
git push origin v2.1.0
gh release create v2.1.0 --title "v2.1.0" --notes-file CHANGELOG.md
```

## Optional

- Link the repository on [Codecov](https://codecov.io) and set `CODECOV_TOKEN` for upload reports.
- Confirm [PyPI](https://pypi.org/project/range-key-dict-2/) shows 2.1.0 after upload (latest on PyPI may still be 2.0.0).
