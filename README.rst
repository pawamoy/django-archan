django-archan
=============

A Django app that displays dependency matrices using `dependenpy`_ Python
module, and also project architecture information, using `archan`_ Python module.

_dependenpy: https://github.com/Pawamoy/dependenpy
_archan: https://github.com/Pawamoy/archan

Installation
------------

Just run:

    pip install django-archan
    
Then add django-archan to the installed apps of your Django project:

.. code:: python

    # settings.py
    
    INSTALLED_APPS += ('darchan')
    
Also add the urls into your main urls.py, something like:

.. code:: python

    # urls.py
    
    ...
    url(r'^darchan/', include('darchan.urls'), name='darchan'),
    ...
    
Usage
-----

*Contents coming later*

Configuration
-------------

The following options are available:

* DARCHAN_PACKAGE_LIST : the list of installed packages that will be scanned to
  build the dependency matrices
* More options coming later
