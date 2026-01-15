from setuptools import setup, Extension
import pybind11
from setuptools import find_packages

# To define C++ extension
ext_modules = []

setup(
    name="Tracking",
    version="0.1.0",
    description="Toy model to show how tracking workings",
    packages=find_packages(where="python"), 
    package_dir={"": "python"},
    ext_modules=ext_modules,
    zip_safe=False,                              
)