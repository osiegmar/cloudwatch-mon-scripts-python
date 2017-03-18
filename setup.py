#!/usr/bin/env python
from cloudwatchmon import VERSION
import os.path

from setuptools import find_packages, setup


def readme():
    path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(path):
        with open(path) as f:
            return f.read()


setup(name='cloudwatchmon',
      version=VERSION,
      description='Linux monitoring scripts for CloudWatch',
      long_description=readme(),
      url='https://github.com/osiegmar/cloudwatch-mon-scripts-python',
      author='Oliver Siegmar',
      author_email='oliver@siegmar.de',
      license='Apache License (2.0)',
      keywords="monitoring cloudwatch amazon web services aws ec2",
      zip_safe=True,
      packages=find_packages(),
      install_requires=['boto>=2.33.0', 'argparse'],
      entry_points={'console_scripts': [
          'mon-get-instance-stats.py=cloudwatchmon.cli.get_instance_stats:main',
          'mon-put-instance-stats.py=cloudwatchmon.cli.put_instance_stats:main',
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: System :: Monitoring'
      ]
      )
