import sys
import refile
from setuptools import setup


install_requires = ['nose']
# pathlib is new to std lib in 3.4
if sys.version_info[:2] < (3, 4):
    install_requires.append('pathlib')


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
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 3'
    ]
)
