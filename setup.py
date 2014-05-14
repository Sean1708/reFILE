import sys
import refile
from setuptools import setup


with open('README.rst', 'w') as readme:
    with open('readme_header.rst', 'r') as head:
        readme.write(head.read())

    with open('refile/__init__.py', 'r') as init:
        init_lines = init.readlines()
        # remove first 4 lines (first line will be blank)
        init_lines = init_lines[4:]
        # write the lines until the dend of docstring is reached
        for line in init_lines:
            if line[:3] == '"""':
                break
            else:
                readme.write(line)


install_requires = ['nose']
# pathlib is new to std lib in 3.4
if sys.version_info[:2] < (3, 4):
    install_requires.append('pathlib')
# argparse is not in 2.6 or lower
if sys.version_info[:2] < (2, 7):
    install_requires.append('argparse')
# it's not in 3.1 either
elif sys.version_info[1] < 2:
    install_requires.append('argparse')


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
