#!/usr/bin/env python
# coding=utf8
import flask
import os
import glob
import sys
from string import Template
import time
import webbrowser
from optparse import OptionParser
import requests
# noinspection PyUnresolvedReferences
from lib.cmdline import parse_args
# noinspection PyUnresolvedReferences
from lib.scancore import AbstractScan
import datetime
args = parse_args()


def main():
    scanner = AbstractScan(args)
    scanner.run()


if __name__ == '__main__':


    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp)
    main()
    timestampend = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestampend)
