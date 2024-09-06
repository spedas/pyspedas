"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encols distding
from codecs import open

setup(
    name="pyspedas",
    version="1.6.0",
    description="Python Space Physics Environment Data Analysis Software (pySPEDAS)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/spedas/pyspedas",
    author="Jim Lewis",
    author_email="jwl@ssl.berkeley.edu",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="spedas data tools",
    project_urls={
        "Information": "http://spedas.org/wiki/",
    },
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        "numpy>=1.20.0",
        "requests",
        "geopack>=1.0.11",
        "scipy",
        "cdflib",
        "cdasws>=1.7.24",
        "netCDF4>=1.6.2",
        "pywavelets",
        "astropy",
        "hapiclient>=0.2.2",
        "pytplot-mpl-temp>=2.2.43",
        "viresclient",
    ],
    python_requires=">=3.9",
    include_package_data=True,
)
