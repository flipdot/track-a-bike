#!/usr/bin/env python3
import threading
from configparser import ConfigParser

import sys
from datetime import datetime

from preprocess import xml2csv
from visualize import free_bikes_timeline, neo4j2dot
from constants import LOG_FORMAT
from collect import dump, compress
import logging
import argparse


# from http://stackoverflow.com/a/14035296/4592067
def set_interval(func, sec, *args, **kwargs):
    def func_wrapper():
        set_interval(func, sec, *args, **kwargs)
        func(*args, **kwargs)

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


last_date = None


def dump_and_compress():
    global last_date
    dump.run()
    current_date = datetime.now().strftime('%Y-%m-%d')
    if last_date is not None and last_date != current_date:
        compress.run(last_date)
    last_date = current_date


def command_collect(args):
    dump_and_compress()
    set_interval(dump_and_compress, args.interval * 60)


def command_preprocess(args):
    print('Not yet implemented')
    pass


def command_visualize(args):
    print('Not yet implemented')
    pass


logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

parser = argparse.ArgumentParser(description='Collect and analyze db rent bikes')
subparsers = parser.add_subparsers(dest='command')
subparsers.required = True

parser_collect = subparsers.add_parser('collect', help='Collect periodically data')
parser_preprocess = subparsers.add_parser('preprocess', help='Converts the raw xml data to csv')
parser_visualize = subparsers.add_parser('visualize', help='Creates various visualizations')

parser_collect.add_argument('--interval', help='Interval in minutes', default=1, type=int)

commands = {
    'collect': command_collect,
    'preprocess': command_preprocess,
    'visualize': command_visualize
}

args = parser.parse_args()
commands[args.command](args)

# xml2csv.run()
# free_bikes_timeline.run()
# neo4j2dot.run()
