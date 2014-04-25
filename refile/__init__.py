"""List, rename and delete files using Python-style regex.

**THIS PROGRAM IS STILL IN THE ALPHA TESTING STAGE SO PLEASE ENSURE THAT YOU
KEEP REGULAR BACKUPS AND DO NOT USE IT ON ANY IMPORTANT DOCUMENTS OR FILES**

The refile command line utility performs three useful tasks on a directory of
files; listing files which match a regular expression, renaming files which
matche a regular expression and deleting files which match a regular
expression.

Usage::

    refile -h
    refile ls [-h] PATTERN [DIR]
    refile mv [-h] PATTERN REPLACE [DIR]
    refile rm [-h] PATTERN [DIR]


General Advice
==============

To avoid issues with variable expansion and special characters on the command
line it is advisable to enclose the regular expression in single quotes::

    refile ls '.*'

without the quotes this would cause a list of all files whose name starts with
a period to be passed to ``refile`` which would, unsurprisingly, lead to
unexpected behaviour.

If no directory is specified, the current directory is searched. A directory
can be specified as an absolute path or a relative one, if an absolute path is
used then filenames will be printed as an absolute path and similarly for
relative paths. Tilde expansion is performed at the command line but not within
the program so wrapping your directory in single quotes is ill-advised.


Listing Files
=============

Usage::

    refile ls [-h] PATTERN [DIR]

The ``ls`` subcommand lists all files in the directory ``DIR`` which match the
regular expression ``PATTERN``. Internally this is run using the ``re.search``
function so the pattern can match any part of the filename, not just the start.

Options
-------

-h, --help              print a useful help message


Renaming Files
==============

Usage::

    refile mv [-h] PATTERN REPLACE [DIR]

The ``mv`` subcommand renames any file in the directory ``DIR`` which matches
the regular expression ``PATTERN`` to the name ``RENAME``. This is run
internally using the ``re.sub`` function.

If ``PATTERN`` matches more than once in the filename then each match will be
replaced by the string ``REPLACE`` providing the matches don't overlap. If the
regular expression matches the entire filename then ``PATTERN`` and ``REPLACE``
must contain groups and backreferences to avoid files overwriting eachother.
This is not checked at run-time so it is up to the user to ensure proper usage.

Options
-------

-h, --help              print a useful help message


Deleting Files
==============

Usage::

    refile rm [-h] PATTERN [DIR]

The ``rm`` subcommand deletes all files in the directory ``DIR`` which match
regular expression ``PATTERN``. The search is performed identically to the
``ls`` subcommand so a good way to ensure that you are deleting the correct
files is to run the command as ``ls`` first.

Options
-------

-h, --help              print a useful help message

"""
