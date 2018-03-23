About tgext.celery
-------------------------

tgext.celery is a TurboGears2 extension that integrates celery into a turbogears application

I tested this extension just with the celery[mongodb]==3.1 bundle of celery and pymongo==3.5.1
using mongodb as both message broker and result backend

integrates both ``celery beat`` and ``celery worker``


Installing
-------------------------------

tgext.celery can be installed from pypi::

    pip install tgext.celery

should just work for most of the users.

Plugging
-------------------------------

To enable tgext.celery put inside your application
``config/app_cfg.py`` the following::

    from tgext.pluggable import plug
    plug(base_config, 'tgext.celery')

put in your ``*.ini`` file the options that you want to pass to your celery application
prefixed by ```celery.```::

    #celery config
    celery.CELERY_TASK_SERIALIZER = json
    celery.CELERY_RESULT_SERIALIZER = json
    celery.CELERY_ACCEPT_CONTENT = json
    celery.CELERY_TIMEZONE = UTC
    celery.BROKER_URL = mongodb://localhost:27017/dbname
    celery.CELERY_RESULT_BACKEND = mongodb://localhost:27017/dbname
    celery.CELERYD_POOL = celery.concurrency.threads.TaskPool
    celery.CELERY_INCLUDE = myproject.lib.celery.tasks
    celery.CELERYD_CONCURRENCY = 3

see http://docs.celeryproject.org/en/3.1/configuration.html#configuration for other options

you can pass other options (that override the other in the .ini file) when plugging this extension
this is convenient because the options in the .ini file aren't evaluated::

    plug(
        base_config,
        'tgext.celery',
        celery_config={
            'CELERY_MONGODB_BACKEND_SETTINGS': {
                'database': 'dbname',
            },
            'CELERYBEAT_SCHEDULE': {
                'delete-unassociated-images-every-12-hours': {
                    'task': 'delete_unassociated_images',
                    'schedule': timedelta(hours=12),
                },
            },
        },
    )

Writing tasks
-------------------------------

Remember to set the ``CELERY_INCLUDE`` option
here's an example with a task::

    from __future__ import absolute_import

    from myproject import model

    from tgext.celery import celery_app

    import logging

    logger = logging.getLogger(__name__)

    celery_app.config_from_object(config['celery_configuration_object'])


    @celery_app.task(name='delete_unassociated_images')
    def delete_unassociated_images():
        logger.info('started')
        model.Image.query.remove({'post_id': None})
        logger.info('finished')

Executing
-------------------------------

``tgext.celery`` sets two gearbox commands, you can run celery with::

    gearbox celeryworker -c production.ini --logfile=/var/log/circus/myproject_celery_worker_tasks.log

and::

    gearbox celerybeat -c production.ini

in a production environment you should put these commands in a circus watcher or supervisord
