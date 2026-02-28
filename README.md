A lost and found desktop app for ECM2429

# uv
[uv](https://docs.astral.sh/uv/) is used to manage dependencies and the virtual environment.
It can be installed [here](https://docs.astral.sh/uv/getting-started/installation/#pypi).

# Run the app
`uv run lost-and-found`

# Run the tests
`uv run pytest --cov=. src/tests/`

# Run flake8
`uv run flake8 src/ --count --max-complexity=5 --statistics`

# Build HTML documentation (must be in docs directory)
`uv run make html`

# Build PDF documentation (must be in docs directory)
`uv run make latexpdf`