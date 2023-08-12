# tifffile/setup.py

"""Tifffile package Setuptools script."""

import sys
import re

from setuptools import setup

buildnumber = ''


def search(pattern, code, flags=0):
    # return first match for pattern in code
    match = re.search(pattern, code, flags)
    if match is None:
        raise ValueError(f'{pattern!r} not found')
    return match.groups()[0]


with open('tifffile/tifffile.py', encoding='utf-8') as fh:
    code = fh.read().replace('\r\n', '\n').replace('\r', '\n')

version = search(r"__version__ = '(.*?)'", code).replace('.x.x', '.dev0')
version += ('.' + buildnumber) if buildnumber else ''

description = search(r'"""(.*)\.(?:\r\n|\r|\n)', code)

readme = search(
    r'(?:\r\n|\r|\n){2}r"""(.*)"""(?:\r\n|\r|\n){2}from __future__',
    code,
    re.MULTILINE | re.DOTALL,
)
readme = '\n'.join(
    [description, '=' * len(description)] + readme.splitlines()[1:]
)

if 'sdist' in sys.argv:
    # update README, LICENSE, and CHANGES files

    with open('README.rst', 'w', encoding='utf-8') as fh:
        fh.write(readme)

    license = search(
        r'(# Copyright.*?(?:\r\n|\r|\n))(?:\r\n|\r|\n)+r""',
        code,
        re.MULTILINE | re.DOTALL,
    )
    license = license.replace('# ', '').replace('#', '')

    with open('LICENSE', 'w', encoding='utf-8') as fh:
        fh.write('BSD 3-Clause License\n\n')
        fh.write(license)

    revisions = search(
        r'(?:\r\n|\r|\n){2}(Revisions.*)- …',
        readme,
        re.MULTILINE | re.DOTALL,
    ).strip()

    with open('CHANGES.rst', encoding='utf-8') as fh:
        old = fh.read()

    old = old.split(revisions.splitlines()[-1])[-1]
    with open('CHANGES.rst', 'w', encoding='utf-8') as fh:
        fh.write(revisions.strip())
        fh.write(old)

setup(
    name='tifffile',
    version=version,
    license='BSD',
    description=description,
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Christoph Gohlke',
    author_email='cgohlke@cgohlke.com',
    url='https://www.cgohlke.com',
    project_urls={
        'Bug Tracker': 'https://github.com/cgohlke/tifffile/issues',
        'Source Code': 'https://github.com/cgohlke/tifffile',
        # 'Documentation': 'https://',
    },
    packages=['tifffile'],
    package_data={'tifffile': ['py.typed']},
    python_requires='>=3.9',
    install_requires=[
        'numpy',
        # 'imagecodecs>=2023.8.12',
    ],
    extras_require={
        'all': [
            'imagecodecs>=2023.8.12',
            'matplotlib',
            'defusedxml',
            'lxml',
            'zarr',
            'fsspec',
        ]
    },
    tests_require=[
        'pytest',
        'imagecodecs',
        'czifile',
        'cmapfile',
        'oiffile',
        'lfdfiles',
        'psdtags',
        'roifile',
        'lxml',
        'zarr',
        'dask',
        'xarray',
        'fsspec',
        'defusedxml',
        'ndtiff',
    ],
    entry_points={
        'console_scripts': [
            'tifffile = tifffile:main',
            'tiffcomment = tifffile.tiffcomment:main',
            'tiff2fsspec = tifffile.tiff2fsspec:main',
            'lsm2bin = tifffile.lsm2bin:main',
        ],
        # 'napari.plugin': ['tifffile = tifffile.napari_tifffile'],
    },
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
