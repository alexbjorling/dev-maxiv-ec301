#!/usr/bin/env python
from setuptools import setup

setup(name = "tangods-regloicc",
      version = "0.0.1",
      description = ("Tango device server for the Ismatec Reglo ICC peristaltic pump."),
      author = "Alexander Bjoerling",
      author_email = "alexander.bjorling@maxiv.lu.se",
      license = "GPLv3",
      url = "http://www.maxiv.lu.se",
      packages = ['regloicc'],
      package_dir = {'':'src'},
      scripts = ['scripts/regloicc']
     )
