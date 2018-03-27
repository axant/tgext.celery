from __future__ import absolute_import
from gearbox.command import Command
from paste.deploy import loadapp
from webtest import TestApp
from os import getcwd

from tgext.celery.celery import celery_app
from tg import config


class CeleryBeatCommand(Command):
    def get_description(self):
        return "Starts Celery beat in turbogears"

    def get_parser(self, prog_name):
        parser = super(CeleryBeatCommand, self).get_parser(prog_name)

        parser.add_argument("-c", "--config",
                            help='application config file to read (default: development.ini)',
                            dest='config_file', default="development.ini")
        return parser

    def take_action(self, opts):
        from celery.apps.beat import Beat
        config_file = opts.config_file
        config_name = 'config:%s' % config_file
        here_dir = getcwd()

        # Load the wsgi app first so that everything is initialized right
        loadapp(config_name, relative_to=here_dir)

        celery_app.config_from_object(config['celery_configuration_object'])
        beat = Beat(app=celery_app)
        beat.start_scheduler()


class CeleryWorkerCommand(Command):
    def get_description(self):
        return "Starts Celery worker in turbogears"

    def get_parser(self, prog_name):
        parser = super(CeleryWorkerCommand, self).get_parser(prog_name)

        parser.add_argument("-c", "--config",
                            help='application config file to read (default: development.ini)',
                            dest='config_file', default="development.ini")

        parser.add_argument('-l', '--logfile',
                            help='path of the log file', default='celery_log.txt')

        parser.add_argument('-L', '--loglevel',
                            help='severity of the log', default='INFO')

        return parser

    def take_action(self, opts):
        from celery.apps.worker import Worker
        config_file = opts.config_file
        config_name = 'config:%s' % config_file
        here_dir = getcwd()

        # Load the wsgi app first so that everything is initialized right
        wsgiapp = loadapp(config_name, relative_to=here_dir)

        # load celery config
        celery_app.config_from_object(config['celery_configuration_object'])
        
        worker = Worker(app=celery_app, logfile=opts.logfile, loglevel=opts.loglevel)
        worker.start()
