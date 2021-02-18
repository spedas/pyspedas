"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

setup(
    name='pyspedas',
    version='1.1.6',
    description='Python Space Physics Environment Data Analysis Software (SPEDAS)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/spedas/pyspedas',
    author='Nick Hatzigeorgiu, Eric Grimes',
    author_email='nikos@berkeley.edu, egrimes@igpp.ucla.edu',
    license='MIT',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 ],
    keywords='spedas data tools',
    project_urls={'Information': 'http://spedas.org/wiki/',
                  },
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['numpy<=1.19.3', 'requests', 'pytplot>=1.7.18',
                      'cdflib>=0.3.20', 'cdasws>=1.7.24', 'netCDF4',
                      'pywavelets', 'pyqtgraph>=0.11.1', 'astropy'],
    python_requires='>=3.6',
    include_package_data=True,
)
