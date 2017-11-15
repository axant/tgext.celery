About tgext.celery
-------------------------

tgext.celery is a TurboGears2 extension that integrate celery into a turbogears application

I tested this extension just with the 


Installing
-------------------------------

tgext.celery can be installed from pypi::

    pip install tgext.celery

should just work for most of the users.

Enabling
-------------------------------

To enable tgext.celery put inside your application
``config/app_cfg.py`` the following::

    import tgext.celery
    tgext.celery.plugme(base_config)

or you can use ``tgext.pluggable`` when available::

    from tgext.pluggable import plug
    plug(base_config, 'tgext.celery')


