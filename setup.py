"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

setup(
    name='pyspedas',
    version='0.8.6',
    description='Python Space Physics Environment Data Analysis \
                    Software (SPEDAS)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/spedas/pyspedas',
    author='Nick Hatzigeorgiu, Eric Grimes',
    author_email='nikos@berkeley.edu',
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 ],
    keywords='spedas data tools',
    project_urls={'Information': 'http://spedas.org/wiki/',
                  },
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['pyqtwebengine', 'pyqt5==5.12', 'requests', 'scipy', 'pytplot>=1.4', 'astropy', 'cdflib', 'msgpack', 'bokeh', 'nodejs',
                      'pyqtgraph', 'numpy', 'pydivide', 'pandas>=0.24'],
    python_requires='>=3.5',
)
