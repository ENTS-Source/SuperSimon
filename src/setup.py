from setuptools import setup

setup(name='ents-supersimon',
      version='1.1',
      description='ENTS SuperSimon master game controller',
      url='https://github.com/ENTS-Source/SuperSimon',
      install_requires=[
          'configobj',
          'pygame',
          'RPi.GPIO',
          'requests',
      ],
      zip_safe=False)
