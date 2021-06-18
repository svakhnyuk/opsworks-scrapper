#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(target): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='target_scraper',
    version='0.1.',
    description="Target Scraper",
    author="Serhiy Vakynyuk",
    packages=find_packages(),
    entry_points={'scrapy': ['settings = opsworks_scraper.settings']},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='target',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    setup_requires=setup_requirements,
)
