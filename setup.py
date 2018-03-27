from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

version = "0.0.3"

setup(
    name='tgext.celery',
    version=version,
    description="",
    long_description=README,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='turbogears2.extension',
    author='Vincenzo Castiglia',
    author_email='vincenzo.castiglia@axant.it',
    url='https://github.com/axant/tgext.celery.git',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages = ['tgext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "TurboGears2 >= 2.3.11",
        "gearbox",
        "PasteDeploy",
        "celery[mongodb]==3.1",
        "threadpool",
    ],
    entry_points={
        'gearbox.commands': [
            'celerybeat = tgext.celery.commands:CeleryBeatCommand',
            'celeryworker = tgext.celery.commands:CeleryWorkerCommand',
        ],
    },
)
