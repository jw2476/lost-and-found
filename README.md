A lost and found desktop app for ECM2429

# Install the dependencies
`pip install -r requirements.txt`

# Install the app (needed to build documentation)
`pip install .`

# Run the app (must be in the src directory)
`python -m lost_and_found`

# Run the tests (must be in the src directory)
`python -m pytest --cov=. tests/`

# Run flake8 (must be in the project root directory)
`python -m flake8 src/ --count --max-complexity=5 --statistics`

# Build HTML documentation (must be in docs directory)
`.\make.bat html`

# Build PDF documentation (must be in docs directory)
`.\make.bat latexpdf`

# Wireframes
Wireframes for the proposed web UI can be found in the `wireframes` directory

# Pre-built documentation
Pre-built documentation can be found in `docs/prebuilt`