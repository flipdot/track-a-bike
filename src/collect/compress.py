#!/usr/bin/env python3

import os
import subprocess
from constants import XML_DIRECTORY
import logging
import shutil


def run(date):
    if not date:
        raise ValueError('"date" must not be empty')
    logging.info('Compressing XML files from {}'.format(date))
    directory_name = date
    archive_name = os.extsep.join([date, 'tar.xz'])
    subprocess.run(['tar', '-cJf', archive_name, directory_name], cwd=XML_DIRECTORY)
    shutil.rmtree(os.path.join(XML_DIRECTORY, directory_name))