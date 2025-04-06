#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Clean previous builds
rm -rf build dist

# Build the application
python setup.py py2app

# Clean up
deactivate
rm -rf venv

echo "Build complete! The application is in dist/The Weather Wire.app" 