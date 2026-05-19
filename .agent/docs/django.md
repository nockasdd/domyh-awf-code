---
library: django
version: 5.x
latest: true
category: backend
official_docs: https://docs.djangoproject.com
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/django/django/contents/docs/topics
---

# settings

===============
Django settings
===============

A Django settings file contains all the configuration of your Django
installation. This document explains how settings work and which settings are
available.

The basics
==========

A settings file is just a Python module with module-level variables.

Here are a couple of example settings::

    ALLOWED_HOSTS = ["www.example.com"]
    DEBUG = False
    DEFAULT_FROM_EMAIL = "webmaster@example.com"

.. note::

    If you set :setting:`DEBUG` to ``False``, you also need to properly set
    the :setting:`ALLOWED_HOSTS` setting.

Because a settings file is a Python module, the following apply:

* It doesn't allow for Python syntax errors.
* It can assign settings dynamically using normal Python syntax.
  For example::

      MY_SETTING = [str(i) for i in range(30)]

* It can import values from other settings files.

.. _django-settings-module:

Designating the settings
========================

.. envvar:: DJANGO_SETTINGS_MODULE

When you use Django, you have to tell it which settings you're using. Do this
by using an environment variable, :envvar:`DJANGO_SETTINGS_MODULE`.

The value of :envvar:`DJANGO_SETTINGS_MODULE` should be in Python path syntax,
e.g. ``mysite.settings``. Note that the settings module should be on the
Python :data:`sys.path`.


The ``django-admin`` utility
----------------------------

When using :doc:`django-admin </ref/django-admin>`, you can either set the
environment variable once, or explicitly pass in the settings module each time
you run the utility.

Example (Unix Bash shell):

.. code-block:: shell

    export DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin runserver

Example (Windows shell):

.. code-block:: doscon

    set DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin runserver

Use the ``--settings`` command-line argument to specify the settings manually:

.. code-block:: shell

    django-admin runserver --settings=mysite.settings

.. _django-admin: ../django-admin/

On the server (``mod_wsgi``)
----------------------------

In your live server environment, you'll need to tell your WSGI
application what settings file to use. Do that with ``os.environ``::

    import os

    os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

Read the :doc:`Django mod_wsgi documentation
</howto/deployment/wsgi/modwsgi>` for more information and other common
elements to a Django WSGI application.

Default settings
================

A Django settings file doesn't have to define any settings if it doesn't need
to. Each setting has a sensible default value. These defaults live in the
module :source:`django/conf/global_settings.py`.

Here's the algorithm Django uses in compiling settings:

* Load settings from ``global_settings.py``.
* Load settings from the specified settings file, overriding the global
  settings as necessary.

Note that a settings file should *not* import from ``global_settings``, because
that's redundant.

Seeing which settings you've changed
------------------------------------

The command ``python manage.py diffsettings`` displays differences between the
current settings file and Django's default settings.

For more, see the :djadmin:`diffsettings` documentation.

Using settings in Python code
=============================

In your Django apps, use settings by importing the object
``django.conf.settings``. Example::

    from django.conf import settings

    if settings.DEBUG:
        # Do something
        ...

Note that ``django.conf.settings`` isn't a module -- it's an object. So
importing individual settings is not possible::

    from django.conf.settings import DEBUG  # This won't work.

Also note that your code should *not* import from either ``global_settings`` or
your own settings file. ``django.conf.settings`` abstracts the concepts of
default settings and site-specific settings; it presents a single interface.
It also decouples the code that uses settings from the location of your
settings.

Altering settings at runtime
============================

You shouldn't alter settings in your applications at runtime. For example,
don't do this in a view::

    from django.conf import settings

    settings.DEBUG = True  # Don't do this!

The only place you should assign to settings is in a settings file.

Security
========

Because a settings file contains sensitive information, such as the database
password, you should make every attempt to limit access to it. For example,
change its file permissions so that only you and your web server's user can
read it. This is especially important in a shared-hosting environment.

Available settings
==================

For a full list of available settings, see the
:doc:`settings reference </ref/settings>`.

Creating your own settings
==========================

There's nothing stopping you from creating your own settings, for your own
Django apps, but follow these guidelines:

* Setting names must be all uppercase.
* Don't reinvent an already-existing setting.

For settings that are sequences, Django itself uses lists, but this is only
a convention.

.. _settings-without-django-settings-module:

Using settings without setting :envvar:`DJANGO_SETTINGS_MODULE`
===============================================================

In some cases, you might want to bypass the :envvar:`DJANGO_SETTINGS_MODULE`
environment variable. For example, if you're using the template system by
itself, you likely don't want to have to set up an environment variable
pointing to a settings module.

In these cases, you can configure Django's settings manually. Do this by
calling:

.. function:: django.conf.settings.configure(default_settings, **settings)

Example::

    from django.conf import settings

    settings.configure(DEBUG=True)

Pass ``configure()`` as many keyword arguments as you'd like, with each keyword
argument representing a setting and its value. Each argument name should be all
uppercase, with the same name as the settings described above. If a particular
setting is not passed to ``configure()`` and is needed at some later point,
Django will use the default setting value.

Configuring Django in this fashion is mostly necessary -- and, indeed,
recommended -- when you're using a piece of the framework inside a larger
application.

Consequently, when configured via ``settings.configure()``, Django will not
make any modifications to the process environment variables (see the
documentation of :setting:`TIME_ZONE` for why this would normally occur). It's
assumed that you're already in full control of your environment in these
cases.

Custom default settings
-----------------------

If you'd like default values to come from somewhere other than
``django.conf.global_settings``, you can pass in a module or class that
provides the default settings as the ``default_settings`` argument (or as the
first positional argument) in the call to ``configure()``.

In this example, default settings are taken from ``myapp_defaults``, and the
:setting:`DEBUG` setting is set to ``True``, regardless of its value in
``myapp_defaults``::

    from django.conf import settings
    from myapp import myapp_defaults

    settings.configure(default_settings=myapp_defaults, DEBUG=True)

The following example, which uses ``myapp_defaults`` as a positional argument,
is equivalent::

    settings.configure(myapp_defaults, DEBUG=True)

Normally, you will not need to override the defaults in this fashion. The
Django defaults are sufficiently tame that you can safely use them. Be aware
that if you do pass in a new default module, it entirely *replaces* the Django
defaults, so you must specify a value for every possible setting that might be
used in the code you are importing. Check in
``django.conf.settings.global_settings`` for the full list.

Either ``configure()`` or :envvar:`DJANGO_SETTINGS_MODULE` is required
----------------------------------------------------------------------

If you're not setting the :envvar:`DJANGO_SETTINGS_MODULE` environment
variable, you *must* call ``configure()`` at some point before using any code
that reads settings.

If you don't set :envvar:`DJANGO_SETTINGS_MODULE` and don't call
``configure()``, Django will raise an ``ImportError`` exception the first time
a setting is accessed.

If you set :envvar:`DJANGO_SETTINGS_MODULE`, access settings values somehow,
*then* call ``configure()``, Django will raise a ``RuntimeError`` indicating
that settings have already been configured. There is a property for this
purpose:

.. attribute:: django.conf.settings.configured

For example::

    from django.conf import settings

    if not settings.configured:
        settings.configure(myapp_defaults, DEBUG=True)

Also, it's an error to call ``configure()`` more than once, or to call
``configure()`` after any setting has been accessed.

It boils down to this: Use exactly one of either ``configure()`` or
:envvar:`DJANGO_SETTINGS_MODULE`. Not both, and not neither.

Calling ``django.setup()`` is required for "standalone" Django usage
--------------------------------------------------------------------

If you're using components of Django "standalone" -- for example, writing a
Python script which loads some Django templates and renders them, or uses the
ORM to fetch some data -- there's one more step you'll need in addition to
configuring settings.

After you've either set :envvar:`DJANGO_SETTINGS_MODULE` or called
``configure()``, you'll need to call :func:`django.setup` to load your
settings and populate Django's application registry. For example::

    import django
    from django.conf import settings
    from myapp import myapp_defaults

    settings.configure(default_settings=myapp_defaults, DEBUG=True)
    django.setup()

    # Now this script or any imported module can use any part of Django it needs.
    from myapp import models

Note that calling ``django.setup()`` is only necessary if your code is truly
standalone. When invoked by your web server, or through :doc:`django-admin
</ref/django-admin>`, Django will handle this for you.

.. admonition:: ``django.setup()`` may only be called once.

    Therefore, avoid putting reusable application logic in standalone scripts
    so that you have to import from the script elsewhere in your application.
    If you can't avoid that, put the call to ``django.setup()`` inside an
    ``if`` block::

        if __name__ == "__main__":
            import django

            django.setup()

.. seealso::

    :doc:`The Settings Reference </ref/settings>`
        Contains the complete list of core and contrib app settings.


---


# install

=====================
How to install Django
=====================

This document will get you up and running with Django.

Install Python
==============

Django is a Python web framework. See :ref:`faq-python-version-support` for
details.

Get the latest version of Python at https://www.python.org/downloads/ or with
your operating system's package manager.

.. admonition:: Python on Windows

    If you are just starting with Django and using Windows, you may find
    :doc:`/howto/windows` useful.

Install Apache and ``mod_wsgi``
===============================

If you just want to experiment with Django, skip ahead to the next
section; Django includes a lightweight web server you can use for
testing, so you won't need to set up Apache until you're ready to
deploy Django in production.

If you want to use Django on a production site, use `Apache`_ with
`mod_wsgi`_. mod_wsgi operates in one of two modes: embedded
mode or daemon mode. In embedded mode, mod_wsgi is similar to
mod_perl -- it embeds Python within Apache and loads Python code into
memory when the server starts. Code stays in memory throughout the
life of an Apache process, which leads to significant performance
gains over other server arrangements. In daemon mode, mod_wsgi spawns
an independent daemon process that handles requests. The daemon
process can run as a different user than the web server, possibly
leading to improved security. The daemon process can be restarted
without restarting the entire Apache web server, possibly making
refreshing your codebase more seamless. Consult the mod_wsgi
documentation to determine which mode is right for your setup. Make
sure you have Apache installed with the mod_wsgi module activated.
Django will work with any version of Apache that supports mod_wsgi.

See :doc:`How to use Django with mod_wsgi </howto/deployment/wsgi/modwsgi>`
for information on how to configure mod_wsgi once you have it
installed.

If you can't use mod_wsgi for some reason, fear not: Django supports many other
deployment options. One is :doc:`uWSGI </howto/deployment/wsgi/uwsgi>`; it
works very well with `nginx`_. Additionally, Django follows the WSGI spec
(:pep:`3333`), which allows it to run on a variety of server platforms.

.. _Apache: https://httpd.apache.org/
.. _nginx: https://nginx.org/
.. _mod_wsgi: https://modwsgi.readthedocs.io/en/develop/

.. _database-installation:

Get your database running
=========================

If you plan to use Django's database API functionality, you'll need to make
sure a database server is running. Django supports many different database
servers and is officially supported with PostgreSQL_, MariaDB_, MySQL_, Oracle_
and SQLite_.

If you are developing a small project or something you don't plan to deploy in
a production environment, SQLite is generally the best option as it doesn't
require running a separate server. However, SQLite has many differences from
other databases, so if you are working on something substantial, it's
recommended to develop with the same database that you plan on using in
production.

In addition to the officially supported databases, there are :ref:`backends
provided by 3rd parties <third-party-notes>` that allow you to use other
databases with Django.

To use another database other than SQLite, you'll need to make sure that the
appropriate Python database bindings are installed:

* If you're using PostgreSQL, you'll need the `psycopg`_ or `psycopg2`_
  package. Refer to the :ref:`PostgreSQL notes <postgresql-notes>` for further
  details.

* If you're using MySQL or MariaDB, you'll need a :ref:`DB API driver
  <mysql-db-api-drivers>` like ``mysqlclient``. See :ref:`notes for the MySQL
  backend <mysql-notes>` for details.

* If you're using SQLite you might want to read the :ref:`SQLite backend notes
  <sqlite-notes>`.

* If you're using Oracle, you'll need to install oracledb_, but please read the
  :ref:`notes for the Oracle backend <oracle-notes>` for details regarding
  supported versions of both Oracle and ``oracledb``.

* If you're using an unofficial 3rd party backend, please consult the
  documentation provided for any additional requirements.

And ensure that the following keys in the ``'default'`` item of the
:setting:`DATABASES` dictionary match your database connection settings:

* :setting:`ENGINE <DATABASE-ENGINE>` -- Either
  ``'django.db.backends.sqlite3'``,
  ``'django.db.backends.postgresql'``,
  ``'django.db.backends.mysql'``, or
  ``'django.db.backends.oracle'``. Other backends are :ref:`also available
  <third-party-notes>`.

* :setting:`NAME` -- The name of your database. If you’re using SQLite, the
  database will be a file on your computer. In that case, ``NAME`` should be
  the full absolute path, including the filename of that file. You don’t need
  to create anything beforehand; the database file will be created
  automatically when needed. The default value, ``BASE_DIR / 'db.sqlite3'``,
  will store the file in your project directory.

.. admonition:: For databases other than SQLite

    If you are not using SQLite as your database, additional settings such as
    :setting:`USER`, :setting:`PASSWORD`, and :setting:`HOST` must be added.
    For more details, see the reference documentation for :setting:`DATABASES`.

    Also, make sure that you've created the database by this point. Do that
    with "``CREATE DATABASE database_name;``" within your database's
    interactive prompt.

If you plan to use Django's ``manage.py migrate`` command to automatically
create database tables for your models (after first installing Django and
creating a project), you'll need to ensure that Django has permission to create
and alter tables in the database you're using; if you plan to manually create
the tables, you can grant Django ``SELECT``, ``INSERT``, ``UPDATE`` and
``DELETE`` permissions. After creating a database user with these permissions,
you'll specify the details in your project's settings file, see
:setting:`DATABASES` for details.

If you're using Django's :doc:`testing framework</topics/testing/index>` to
test database queries, Django will need permission to create a test database.

.. _PostgreSQL: https://www.postgresql.org/
.. _MariaDB: https://mariadb.org/
.. _MySQL: https://www.mysql.com/
.. _psycopg: https://www.psycopg.org/psycopg3/
.. _psycopg2: https://www.psycopg.org/
.. _SQLite: https://www.sqlite.org/
.. _oracledb: https://oracle.github.io/python-oracledb/
.. _Oracle: https://www.oracle.com/

.. _install-django-code:

Install the Django code
=======================

Installation instructions are slightly different depending on whether you're
installing a distribution-specific package, downloading the latest official
release, or fetching the latest development version.

.. _installing-official-release:

Installing an official release with ``pip``
-------------------------------------------

This is the recommended way to install Django.

#. Install pip_. The easiest is to use the `standalone pip installer`_. If your
   distribution already has ``pip`` installed, you might need to update it if
   it's outdated. If it's outdated, you'll know because installation won't
   work.

#. Take a look at :doc:`venv <python:tutorial/venv>`. This tool provides
   isolated Python environments, which are more practical than installing
   packages systemwide. It also allows installing packages without
   administrator privileges. The :doc:`contributing tutorial
   </intro/contributing>` walks through how to create a virtual environment.

#. After you've created and activated a virtual environment, enter the command:

   .. console::

        $ python -m pip install Django

.. _pip: https://pip.pypa.io/
.. _standalone pip installer: https://pip.pypa.io/en/latest/installation/

.. _installing-distribution-package:

Installing a distribution-specific package
------------------------------------------

Check the :doc:`distribution specific notes </misc/distributions>` to see if
your platform/distribution provides official Django packages/installers.
Distribution-provided packages will typically allow for automatic installation
of dependencies and supported upgrade paths; however, these packages will
rarely contain the latest release of Django.

.. _installing-development-version:

Installing the development version
----------------------------------

.. admonition:: Tracking Django development

    If you decide to use the latest development version of Django,
    you'll want to pay close attention to `the development timeline`_,
    and you'll want to keep an eye on the :ref:`release notes for the
    upcoming release <development_release_notes>`. This will help you stay
    on top of any new features you might want to use, as well as any changes
    you'll need to make to your code when updating your copy of Django.
    (For stable releases, any necessary changes are documented in the
    release notes.)

.. _the development timeline: https://code.djangoproject.com/timeline

If you'd like to be able to update your Django code occasionally with the
latest bug fixes and improvements, follow these instructions:

#. Make sure that you have Git_ installed and that you can run its commands
   from a shell. (Enter ``git help`` at a shell prompt to test this.)

#. Check out Django's main development branch like so:

   .. console::

        $ git clone https://github.com/django/django.git

   This will create a directory ``django`` in your current directory.

#. Make sure that the Python interpreter can load Django's code. The most
   convenient way to do this is to use a virtual environment and pip_. The
   :doc:`contributing tutorial </intro/contributing>` walks through how to
   create a virtual environment.

#. After setting up and activating the virtual environment, run the following
   command:

   .. console::

        $ python -m pip install -e django/

   This will make Django's code importable, and will also make the
   ``django-admin`` utility command available. In other words, you're all
   set!

When you want to update your copy of the Django source code, run the command
``git pull`` from within the ``django`` directory. When you do this, Git will
download any changes.

.. _Git: https://git-scm.com/


---
