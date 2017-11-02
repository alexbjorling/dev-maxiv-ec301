#!/usr/bin/env python
from setuptools import setup

setup(name = "tangods-ec301",
      version = "0.0.1",
      description = ("Tango device server for the SRS EC301 potentiostat/galvanostat."),
      author = "Alexander Bjoerling",
      author_email = "alexander.bjorling@maxiv.lu.se",
      license = "GPLv3",
      url = "http://www.maxiv.lu.se",
      packages = ['ec301'],
      package_dir = {'':'src'},
      scripts = ['scripts/ec301']
     )
