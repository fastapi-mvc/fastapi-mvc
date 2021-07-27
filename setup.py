# -*- coding: utf-8 -*-
"""Setup file configuration."""
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
exec(open('fastapi_mvc_template/version.py').read())

setup(
    name='fastapi_mvc_template',
    version=__version__,
    description='FastAPI project core implemented using MVC architectural '
                'pattern with base utilities, tests, and pipeline to speed '
                'up creating new projects based on FastAPI.',
    url='https://github.com/rszamszur/fastapi-mvc-template',
    author='Radosław Szamszur',
    author_email='radoslawszamszur@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: FastAPI MVC template',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    install_requires=[
        "uvicorn[standard]==0.14.0",
        "fastapi>=0.66.0,<0.67.0",
        "starlette>=0.14.2",
        "pydantic>=1.8.2",
        "gunicorn>=20.1.0,<20.2.0",
        "aioredis==2.0.0a1",
        "aiohttp>=3.7.0,<4.0.0",
        "click>=7.1.2",
    ],
    entry_points={
        'console_scripts': [
            'fastapi=fastapi_mvc_template.cli.cli:cli',
        ],
    },

)
