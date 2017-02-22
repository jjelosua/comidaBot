#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from fabric.api import local, require, settings, task, execute
import shutil
import os
import logging
import zipfile

"""
Logging
"""
LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s: %(message)s'
LOG_LEVEL = logging.INFO

# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


def add_code_to_zip(venvpath='venv'):
    """
    Creates a zipfile with code and needed libraries
    """
    INPUT_PATH = os.path.join(cwd, 'code')
    OUTPUT_PATH = os.path.join(cwd, 'zip')
    with zipfile.ZipFile('%s/lambda.zip' % OUTPUT_PATH, 'a') as z:
        z.write('%s/requirements.txt' % INPUT_PATH, 'requirements.txt')
        z.write('%s/bot.py' % INPUT_PATH, 'bot.py')


@task
def deploy(function='comidaBot'):
    """
    Deploy lambda code to AWS
    - Compress code folder
    """
    # Libraries to include
    INPUT_PATH = os.path.join(cwd, 'code/venv/lib/python2.7/site-packages')
    OUTPUT_PATH = os.path.join(cwd, 'zip')
    try:
        # Create output files folder if needed
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        # Get the list of all folders present within the particular directory
        shutil.make_archive('%s/lambda' % (OUTPUT_PATH), 'zip', INPUT_PATH)
        add_code_to_zip()
    except Exception, e:
        logger.error("Exit with uncaptured exception %s" % (e))
        raise
    command = 'aws lambda update-function-code'
    command += ' --zip-file=fileb://zip/lambda.zip'
    command += ' --function-name %s' % (function)
    local(command)
