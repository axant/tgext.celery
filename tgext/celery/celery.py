from __future__ import absolute_import

from celery import Celery
from celery.backends.mongodb import MongoBackend
from celery.loaders.app import AppLoader


class TgCeleryAppLoader(AppLoader):
    override_backends = {
        'mongodb': 'tgext.celery.celery:TgMongoBackend',
    }


class TgMongoBackend(MongoBackend):
    def __init__(self, *args, **kwargs):
        super(TgMongoBackend, self).__init__(*args, **kwargs)
        self.options.pop('max_pool_size', None)
        self.options.pop('auto_start_request', None)


celery_app = Celery('celery_app', loader=TgCeleryAppLoader)
