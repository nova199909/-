#!/usr/bin/env python
# coding=utf8

import argparse
import sys
import os

p_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check_args(args):
    """if not args.m:
        msg = 'Use -m to set attack Mode'
        raise Exception(msg)"""
    if args.autoIP and args.autoURL:
        msg = 'Only use one auto method'
        raise Exception(msg)
    if not args.autoIP and not args.autoURL:
        if not args.u and not args.i:
            msg = 'You should choose a method assign a file'
            raise Exception(msg)
    if args.u and args.i:
        msg = 'Only use -u or -i assign a file'
        raise Exception(msg)
    """if args.u and not os.path.isfile(args.u):
        msg = 'TargetFile not found: %s' %args.u
        raise Exception(msg)"""
    if args.i and not os.path.isfile(args.i):
        msg = 'TargetFile not found: %s' % args.i
        raise Exception(msg)



def parse_args():
    parser = argparse.ArgumentParser(prog='xuptscan',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='* batch vulnerability verification and exploition framework. *\nBy '
                                                 'zhai',
                                     usage='xuptscan.py [options]')
    parser.add_argument('-u', metavar='URL', type=str, default='',
                        help='The target url you set')
    parser.add_argument('-w', metavar='filename-level', type=str, default='small',
                        help='The word-list you set, We offer three different options:large,medium,small'
                             'large.txt.eg:-w large')
    parser.add_argument('-c', metavar='cookies', type=str, default='',
                        help='Some web need cookies,you should set it')
    parser.add_argument('-t', metavar='THREADS', type=int, default=10,
                        help='Num of scan threads for each scan process, 10 by default')
    parser.add_argument('-d', metavar='Delay', type=int, default=0,
                        help='The Delay you set, 0s by default')
    parser.add_argument('-l', metavar='URL_FILE', type=str, default='',
                        help='input url file')
    parser.add_argument('-i', metavar='IP_FILE', type=str, default='',
                        help='input ip file')
    parser.add_argument('-autoIP', action='store_true',
                        help='get ip from space search engine and auto attack')
    parser.add_argument('-autoURL', action='store_true',
                        help='get url from space search engine and auto attack')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0    By zhai')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    check_args(args)
    return args
