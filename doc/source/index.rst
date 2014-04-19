
Welcome to zqtable's documentation!
===================================

Zqtable is an (almost) pure Python class that is intended to represent tabular and time-sequence data in memory. 

Zqtable is built with an emphasis on simplicity, both in interface and internal design rather than performance or scalability.

Before choosing this package you might wish to consider alternatives such as Pandas.

About this project
------------------

* Documentation: https://pythonhosted.org/zqtable/
* Released version: https://pypi.python.org/pypi/zqtable/
* Source code: https://bitbucket.org/salimfadhley/zqtable
* Problems, Suggestions & Bugs: sal@stodge.org

Installation
------------

Egg-files for this project are hosted on PyPi. Most Python users should be able to use pip or setuptools to automatically install this project.

Most users can do the following:
::
    pip install jenkinsapi

Or..
::
    easy_install jenkinsapi

You can also install this project from source. Check ou the code from mercurial
and then build the project.

::
    hg clone https://salimfadhley@bitbucket.org/salimfadhley/zqtable <project dir>
    cd <project dir>
    python setup.py install


The Table Class
---------------

.. automodule:: zqtable
    :members: Table, DerivedTable
    :undoc-members:
    :show-inheritance:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

