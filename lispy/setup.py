#! /usr/bin/python3

from setuptools import setup, find_packages

setup(name='lispy',
      version='1.0',
      description='Python LISP Internet Groper',
      author='Moraux Tom && S.J.M. Steffann (https://github.com/steffann/pylisp)',
      author_email='morauxtom@gmai.com',
      packages=['lispy', 'lispy.ip', 'lispy.lisp'],
      
      scripts=['pylig.py'],
      install_requires=['bitstring', 'netifaces', 'ipaddress']
     )
