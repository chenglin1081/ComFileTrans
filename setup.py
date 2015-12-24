# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from com_tf import version

setup(
        name='com_tf',
        version=version,
        description='Togeek file transfer with com',
        classifiers=['Programming Language :: Python :: 3.4'],
        packages=find_packages(),
        include_package_data=True,
        install_requires=['pyserial'],
        entry_points={'console_scripts': ['comtf=com_tf:main']}
)
