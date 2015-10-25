import sys
import refile
from setuptools import setup


install_requires = ['nose']
# pathlib is new to std lib in 3.4
if sys.version_info[:2] < (3, 4):
    install_requires.append('pathlib2')
# argparse is not in 2.6 or lower
if sys.version_info[:2] < (2, 7):
    install_requires.append('ordereddict')
    install_requires.append('argparse')
# it's not in 3.1 either
elif sys.version_info[1] < 2:
    install_requires.append('argparse')

if sys.version_info < (2, 7):
    import unittest  # noqa
    if 'nosetests' in sys.argv:
        import unittest2
        sys.modules['unittest'] = unittest2

setup(
    name=refile.__title__,
    version=refile.__version__,
    author=refile.__author__,
    author_email=refile.__email__,
    description=refile.__description__,
    long_description=open('README.rst').read(),
    url=refile.__homepage__,
    download_url=refile.__download__,
    install_requires=install_requires,
    packages=['refile'],
    entry_points={
        'console_scripts': ['refile = refile.cmdline:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
