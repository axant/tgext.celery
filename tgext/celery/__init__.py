from tg.configuration import milestones
try:
    from celery.app.defaults import _TO_NEW_KEY
except ImportError:
    _TO_NEW_KEY = []


import logging
log = logging.getLogger('tgext.celery')


# This is the entry point of your extension, will be called
# both when the user plugs the extension manually or through tgext.pluggable
# What you write here has the same effect as writing it into app_cfg.py
# So it is possible to plug other extensions you depend on.
def plugme(configurator, options=None, **kwargs):
    if options is None:
        options = {}
    options.update(kwargs)

    log.info('Setting up tgext.celery extension...')
    milestones.config_ready.register(SetupExtension(configurator, options))

    # This is required to be compatible with the
    # tgext.pluggable interface
    return dict(appid='tgext.celery')


# Most of your extension initialization should probably happen here,
# where it's granted that .ini configuration file has already been loaded
# in tg.config but you can still register hooks or other milestones.
class SetupExtension(object):
    def __init__(self, configurator, options):
        self.configurator = configurator
        self.celery_config = options.get('celery_config')

    def __call__(self):
        from tg import config
        from tg.support.converters import aslist, asint, asbool
        from tg.configuration.utils import coerce_config
        config['celery_configuration_object'] = (coerce_config(config, 'celery.', {
            'CELERY_INCLUDE': aslist,
            'CELERY_ACCEPT_CONTENT': aslist,
            'CELERYD_CONCURRENCY': asint,
            'CELERY_EAGER_PROPAGATES_EXCEPTIONS': asbool,
        }))
        config['celery_configuration_object'].update(self.celery_config)
        for k in list(config['celery_configuration_object'].keys()):
            if k in _TO_NEW_KEY:
                config['celery_configuration_object'][_TO_NEW_KEY[k]] = config['celery_configuration_object'][k]
                del config['celery_configuration_object'][k]

    def on_startup(self):
        log.info('+ Application Running!')
