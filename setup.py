from os.path import dirname, realpath, exists
from setuptools import setup, find_packages
import sys


author = u"Paul Müller"
authors = [author]
description = 'in-silico sinograms (phase and fluorescence) of cells'
name = 'cellsino'
year = "2019"

sys.path.insert(0, realpath(dirname(__file__))+"/"+name)
from _version import version

setup(
    name=name,
    author=author,
    author_email='dev@craban.de',
    url='https://github.com/RI-imaging/cellsino',
    version=version,
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license="MIT",
    description=description,
    long_description=open('README.rst').read() if exists('README.rst') else '',
    install_requires=["h5py>=2.7.0",
                      "qpimage",
                      "qpsphere>=0.5.0",
                      "numpy>=1.12.0",
                      ],
    setup_requires=['pytest-runner'],
    tests_require=["pytest"],
    python_requires='>=3.6, <4',
    keywords=["phase microscopy",
              "fluorescence imaging",
              "optical tomography",
              "diffraction tomography",
              ],
    classifiers= [
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research'
                 ],
    platforms=['ALL'],
    )
