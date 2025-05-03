#!/bin/bash
# Script to set up a fresh conda environment for OpenPTV Python

# Create a new conda environment
conda create -y -n openptv2 python=3.11

# Activate the environment
conda activate openptv2

# Install core dependencies with specific versions
conda install -y numpy=1.26.4
conda install -y scipy cython pyyaml

# Install GUI dependencies
conda install -y -c conda-forge traits traitsui chaco enable pyface

# Install additional dependencies
conda install -y matplotlib
conda install -y -c conda-forge pytest pytest-cov black flake8

# Install PySide6 for GUI backend
pip install pyside6

# Install the package in development mode
pip install -e .

# Build the Cython extensions
python setup.py build_ext --inplace

# Verify installation
python -c "import openptv; print(f'OpenPTV installed. Using Cython: {openptv.using_cython()}')"

echo "OpenPTV2 conda environment setup complete!"