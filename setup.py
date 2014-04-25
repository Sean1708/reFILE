from setuptools import setup

setup(
    name='reFILE',
    description='Utility for manipulating files via regex.',
    long_description=open('README.rst').read(),
    author='Sean Marshallsay',
    author_email='srm.1708@gmail.com',
    url='https://github.com/Sean1708/reFILE.git',
    version='0.0',
    install_requires=['nose'],
    packages=['refile'],
    entry_points={
        'console_scripts': ['refile = refile.cmdline:main']
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
