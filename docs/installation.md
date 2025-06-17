# Installation Guide

This guide covers different ways to install and set up the Journalist library.

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation Methods

### Method 1: Using pip (Recommended for Users)

```bash
# Install the latest version from PyPI
pip install journalist

# Install with optional newspaper3k support
pip install journalist[newspaper]

# Install all optional dependencies
pip install journalist[all]
```

### Method 2: Using Poetry (Recommended for Development)

```bash
# Add to existing Poetry project
poetry add journalist

# With optional dependencies
poetry add journalist[all]
```

### Method 3: Development Installation

#### Using Poetry

```bash
# Clone the repository
git clone https://github.com/username/journalist.git
cd journalist

# Install development dependencies
poetry install --with dev

# Activate virtual environment
poetry shell
```

#### Using pip-tools

```bash
# Clone the repository
git clone https://github.com/username/journalist.git
cd journalist

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install pip-tools
pip install pip-tools

# Compile and install dependencies
pip-compile requirements.in --output-file requirements.txt
pip install -r requirements.txt

# For development dependencies (if using requirements-dev.in)
pip-compile requirements-dev.in --output-file requirements-dev.txt
pip install -r requirements-dev.txt
```

## Verification

Test your installation:

```python
import asyncio
from journalist import Journalist

async def test_installation():
    journalist = Journalist(persist=False)
    print(f"Journalist installed successfully!")
    print(f"Session ID: {journalist.session_id}")

asyncio.run(test_installation())
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'journalist'**

- Make sure you activated your virtual environment
- Verify the installation with `pip list | grep journalist`

**ModuleNotFoundError: No module named 'lxml'**

- Install lxml separately: `pip install lxml`
- On some systems, you may need system dependencies

**SSL Certificate errors**

- Update certificates: `pip install --upgrade certifi`
- Or use `--trusted-host` flag during installation

### Platform-Specific Notes

#### Windows

```bash
# Use Windows path separators
.venv\Scripts\activate
```

#### Linux/Mac

```bash
# May need to install system dependencies for lxml
sudo apt-get install libxml2-dev libxslt-dev  # Ubuntu/Debian
brew install libxml2 libxslt  # macOS
```

## Next Steps

- Read the [Quick Start Guide](quickstart.md)
- Explore [Examples](examples.md)
- Check [Configuration Options](configuration.md)
