
import os
from setuptools import setup

setup(
  name = "testsuite-runner",
  packages=['tsr'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = (""),
  license = "Apache 2.0",
  keywords = [],
  url = "https://github.com/fvutils/testsuite-runner",
  entry_points={
    'console_scripts': [
      'tsr = tsr.__main__:main'
    ]
  },
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[
    'jinja2>=2.10'
  ],
)

