#!/usr/bin/env python3
import threading

from preprocess import xml2csv
from visualize import free_bikes_timeline, neo4j2dot
import argparse


# from http://stackoverflow.com/a/14035296/4592067
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


parser = argparse.ArgumentParser(description='Collect and analyze db rent bikes')
parser.add_subparsers()

xml2csv.run()
# free_bikes_timeline.run()
# neo4j2dot.run()
