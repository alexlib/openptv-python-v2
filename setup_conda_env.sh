#!/bin/bash
# Script to set up a fresh conda environment for OpenPTV Python

# Create a new conda environment
conda create -y -n openptv2 python=3.11

# Source conda to make activate command available
eval "$(conda shell.bash hook)"

# Activate the environment
conda activate openptv2

# Install the package in development mode with GUI dependencies
pip install -e .[gui]

# Build the Cython extensions
# python setup.py build_ext --inplace

# Verify installation
python -c "import openptv; print(f'OpenPTV installed. Using Cython: {openptv.using_cython()}')"

echo "OpenPTV2 conda environment setup complete!"
