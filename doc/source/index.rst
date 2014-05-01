toytable: Lightweight python tables 
===================================

.. image:: toy_table.png

Toytable is a lightweight python table library. It provides a class called Table  which is suitable for representing one-dimensional tables (e.g. time-sequences).

Toytable is built with an emphasis on simplicity, both in interface and internal design
rather than performance or scalability. Toytable is intended to have as few dependancies
as possible, and is therefore suitable for casual development tasks.

Toytable is not complete. If you require a higher performance, more feature-rich table class, please
consider `Pandas`_, a very mature project which was a significant inspiration for this project. 

.. _Pandas: http://pandas.pydata.org/

Contents
========

.. toctree::
   :maxdepth: 2

   examples.rst
   aggregations.rst
   tdd.rst
   toytable.table.rst


Useful Links
------------

* Documentation: http://toytable.readthedocs.org/
* Releases: https://pypi.python.org/pypi/toytable/
* Source code: https://bitbucket.org/salimfadhley/toytable
* Issues: https://bitbucket.org/salimfadhley/toytable/issues
* Python 3.3 build status: https://drone.io/bitbucket.org/salimfadhley/toytable
* Python 2.7 build status: https://www.codeship.io/projects/19984

Project Status
--------------

.. image:: https://drone.io/bitbucket.org/salimfadhley/toytable/status.png
   :target: https://drone.io/bitbucket.org/salimfadhley/toytable

.. image:: https://pypip.in/wheel/toytable/badge.png
        :target: https://pypi.python.org/pypi/toytable/

.. image:: https://pypip.in/license/toytable/badge.png
        :target: https://pypi.python.org/pypi/toytable/

.. image:: https://pypip.in/download/toytable/badge.png
    :target: https://pypi.python.org/pypi//toytable/

Installation
------------

Egg-files for this project are hosted on PyPi. Most Python users should be able to use pip or setuptools to automatically install this project.

Most users can do the following:
::
    pip install toytable

Or..
::
    easy_install toytable

You can also install this project from source. Check ou the code from mercurial
and then build the project.

The Table Class
---------------

The Table class (toytable.Table) is the most important component of this package.
It is intended to represent a 'normal' table - that is one which has no 
special colums or has not undergone any transformations (e.g. project, expand).

.. automethod:: toytable.Table.__init__

.. automodule:: toytable
    :members: Table, DerivedTable
    :undoc-members:
    :show-inheritance:

Table Literals
--------------

.. autofunction:: toytable.table_literal

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

