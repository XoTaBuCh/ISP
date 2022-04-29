from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="xotab_serialization",
    version="0.1.0",
    description="Serialization library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XoTaBuCh/ISP",
    author="XoT@B",
    author_email="tanzanit2003@gmail.com",
    license="BSUIR",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSUIR License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["frozendict~=2.3.1", "salt~=3004.1", "PyYAML~=5.4.1"]
)