import imp
import os
import logging

conf_file = os.environ.get('DOCKER_WORKER_CONFIG')


if not conf_file:
    logging.info("Environment variable $DOCKER_WORKER_CONFIG is not set.")


config = imp.new_module('config')
config.__file__ = conf_file

try:
    with open(conf_file) as config_file:
        exec (compile(config_file.read(), conf_file, 'exec'), config.__dict__)
except IOError as e:
    e.strerror = 'Unable to load configuration file (%s)' % e.strerror
    raise
