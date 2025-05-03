@echo off
REM Script to set up a fresh conda environment for OpenPTV Python

REM Create a new conda environment
call conda create -y -n openptv2 python=3.10

REM Activate the environment
call conda activate openptv2

REM Install core dependencies with specific versions
call conda install -y numpy=1.26.4
call conda install -y scipy cython

REM Install GUI dependencies
call conda install -y -c conda-forge traits traitsui chaco enable pyface

REM Install additional dependencies
call conda install -y matplotlib
call conda install -y -c conda-forge pytest pytest-cov black flake8

REM Install PySide6 for GUI backend
pip install pyside6

REM Install the package in development mode
pip install -e .

REM Build the Cython extensions
python setup.py build_ext --inplace

REM Verify installation
python -c "import openptv; print(f'OpenPTV installed. Using Cython: {openptv.using_cython()}')"

echo OpenPTV2 conda environment setup complete!