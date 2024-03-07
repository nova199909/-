from multiprocessing.dummy import Namespace
import argparse

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from arjun.core.colors import green, end, info, bad, good, run, res
import os
import argparse
import json
# from multiprocessing.dummy import Namespace
from urllib.parse import urlparse
import arjun.core.config as mem
from arjun.core.bruter import bruter
from arjun.core.exporter import exporter
from arjun.core.requester import requester
from arjun.core.anomaly import define, compare
from arjun.core.utils import fetch_params, stable_request, random_str, slicer, confirm, populate, reader, nullify, \
    prepare_requests, compatible_path

from arjun.plugins.heuristic import heuristic

arjun_dir = compatible_path(mem.__file__.replace(compatible_path('/core/config.py'), ''))
try:
    from concurrent.futures import ThreadPoolExecutor, as_completed
except ImportError:
    print('%s Please use Python > 3.2 to run.' % bad)
    quit()


def narrower(request, factors, param_groups):
    """
    takes a list of parameters and narrows it down to parameters that cause anomalies
    returns list
    """
    anomalous_params = []
    threadpool = ThreadPoolExecutor(max_workers=mem.var['threads'])
    futures = (threadpool.submit(bruter, request, factors, params) for params in param_groups)
    for i, result in enumerate(as_completed(futures)):
        if result.result():
            anomalous_params.extend(slicer(result.result()))
        if mem.var['kill']:
            return anomalous_params
        #print('%s Processing chunks: %i/%-6i' % (info, i + 1, len(param_groups)), end='\r')
    return anomalous_params


def initialize(request, wordlist, single_url=False):
    """
    handles parameter finding process for a single request object
    returns 'skipped' (on error), list on success
    """
    url = request['url']
    if not url.startswith('http'):
        print('%s %s is not a valid URL' % (bad, url))
        return 'skipped'
    request['url'] = stable_request(url, request['headers'])
    if not request['url']:
        return 'skipped'
    else:
        fuzz = random_str(6)
        response_1 = requester(request, {fuzz: fuzz[::-1]})
        fuzz = random_str(6)
        response_2 = requester(request, {fuzz: fuzz[::-1]})
        factors = define(response_1, response_2, fuzz, fuzz[::-1], wordlist)
        found, words_exist = heuristic(response_1, wordlist)
        if found:
            num = len(found)
            if words_exist:
                print('%s Heuristic scanner found %i parameters' % (good, num))
            else:
                s = 's' if num > 1 else ''
                print('%s Heuristic scanner found %i parameter%s: %s' % (good, num, s, ', '.join(found)))
        if single_url:
            print('%s Logicforcing the URL endpoint' % run)
        populated = populate(wordlist)
        with open(f'{arjun_dir}/db/special.json', 'r') as f:
            populated.update(json.load(f))
        param_groups = slicer(populated, int(len(wordlist) / mem.var['chunks']))
        prev_chunk_count = len(param_groups)
        last_params = []
        while True:
            param_groups = narrower(request, factors, param_groups)
            if len(param_groups) > prev_chunk_count:
                response_3 = requester(request, {fuzz: fuzz[::-1]})
                if compare(response_3, factors, {fuzz: fuzz[::-1]}) != '':
                    return []
            if mem.var['kill']:
                return 'skipped'
            param_groups = confirm(param_groups, last_params)
            prev_chunk_count = len(param_groups)
            if not param_groups:
                break
        confirmed_params = []
        for param in last_params:
            reason = bruter(request, factors, param, mode='verify')
            if reason:
                name = list(param.keys())[0]
                confirmed_params.append(name)
        return confirmed_params


def get_value(url, method, value_list, scan_thread):
    current_path = os.getcwd()
    args = argparse.Namespace(burp_port=None, chunks=500, delay=0, disable_redirects=False, headers=None,
                              import_file=None, include={}, json_file=None, method=method, passive=None, quiet=False,
                              stable=False, text_file=None,
                              threads=scan_thread, timeout=15, url=url,
                              wordlist=current_path+'\\get_value\\db\\'+value_list+".txt")
    mem.var = vars(args)

    mem.var['method'] = mem.var['method'].upper()
    if mem.var['stable'] or mem.var['delay']:
        mem.var['threads'] = 1
    try:
        wordlist_file = args.wordlist
        wordlist_file = compatible_path(wordlist_file)
        wordlist = set(reader(wordlist_file, mode='lines'))
        if mem.var['passive']:
            host = mem.var['passive']
            if host == '-':
                host = urlparse(args.url).netloc
            passive_params = fetch_params(host)
            wordlist.update(passive_params)
        wordlist = list(wordlist)
    except FileNotFoundError:
        exit('%s The specified file for parameters doesn\'t exist' % bad)

    if len(wordlist) < mem.var['chunks']:
        mem.var['chunks'] = int(len(wordlist) / 2)

    if not args.url and not args.import_file:
        exit('%s No target(s) specified' % bad)

    request = prepare_requests(args)

    final_result = {}
    if type(request) == dict:
        # in case of a single target
        mem.var['kill'] = False
        url = request['url']
        these_params = initialize(request, wordlist, single_url=True)
        if these_params == 'skipped':
            return False, "f"
        elif these_params:
            final_result[url] = {}
            final_result[url]['params'] = these_params
            final_result[url]['method'] = request['method']
            final_result[url]['headers'] = request['headers']
            exporter(final_result)
            print(these_params)
            # print(type((final_result[url]['params'])))
            return True, final_result[url]['params']
        else:
            #print('%s No parameters were discovered.' % info)
            return False, "f"
    elif type(request) == list:
        # in case of multiple targets
        count = 0
        for each in request:
            count += 1
            url = each['url']
            mem.var['kill'] = False
            #print('%s Scanning %d/%d: %s' % (run, count, len(request), url))
            these_params = initialize(each, list(wordlist))
            if these_params == 'skipped':
                #print('%s Skipped %s due to errors' % (bad, url))
                return False, "f"
            elif these_params:
                final_result[url] = {}
                final_result[url]['params'] = these_params
                final_result[url]['method'] = each['method']
                final_result[url]['headers'] = each['headers']
                exporter(final_result)
                #print('%s Parameters found: %s\n' % (good, ', '.join(final_result[url]['params'])))
                # print(type((final_result[url]['params'])))  #calss_list
                return True, final_result[url]['params']
            else:
                #print('%s No parameters were discovered.\n' % info)
                return False, "f"

# arguments to be parsed
