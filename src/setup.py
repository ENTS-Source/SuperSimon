from setuptools import setup

setup(name='ents-supersimon',
      version='1.0',
      description='ENTS SuperSimon master game controller',
      url='https://github.com/turt2live/ENTS-SuperSimon',
      install_requires=[
          'RPi.GPIO',
          'configobj'
      ],
      zip_safe=False)
