#coding:utf-8

import os
import sys
import json
import time
import copy

import subprocess
import urllib2
import exceptions
import re

CONNECT_TIMEOUT = 10

def _exec(cmd, in_arg=None):
    if type(cmd) is not str:
        return -1, None, None

    proc = subprocess.Popen(cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    stdout = None
    stderr = None
    if in_arg:
        stdout, stderr = proc.communicate(in_arg)
    else:
        stdout, stderr = proc.communicate()

    return proc.returncode, stdout, stderr


def call(cmd, in_arg=None):
    retcode, stdout, stderr = _exec(cmd, in_arg)
    return retcode


def check_output(cmd, in_arg=None):
    retcode, stdout, stderr = _exec(cmd, in_arg)
    return retcode, stdout


def get_url_lines(url):
    req = urllib2.Request(url,headers={'User-Agent' : "Magic Browser"})
    resp = urllib2.urlopen(req,timeout=CONNECT_TIMEOUT)
    return resp.readlines()

def get_url_content(url):
    req = urllib2.Request(url,headers={'User-Agent' : "Magic Browser"})
    resp = urllib2.urlopen(req,timeout=CONNECT_TIMEOUT)
    return resp.read()

def get_url_json(url):
    return json.loads(get_url_content(url))

def print_script_result(output):
    print json.dumps(output),
    sys.stdout.flush()


def time_in_millisecond():
    return int(time.time() * 1000)


def convert_to_num(value):
    """
    Unit Conversion

    "1K" or "1k" -> 1024
    "1M" or "1m" -> 1024 * 1024
    "1G" or "1g" -> 1024 * 1024 * 1024
    """

    if isinstance(value, (int, long, float)):
        return value

    if type(value) is not str:
        return -1

    rate = 1
    if value.endswith('K') or value.endswith('k'):
        rate = 1024
    elif value.endswith('M') or value.endswith('m'):
        rate = 1024 * 1024
    elif value.endswith('G') or value.endswith('g'):
        rate = 1024 * 1024 * 1024

    value = value if rate == 1 else value[:-1]
    try:
        return int(value) * rate
    except:
        return float(value) * rate

def write_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)

def append_file(fname, content):
    with open(fname, "a") as f:
        f.write(content)

def read_lines(fname):
    lines=None
    try:
        with open(fname, "r") as f:
            lines = f.readlines()
        if lines is not None:
            ret = [];
            for line in lines:
                line = line.strip();
                if line == "":
                    continue
                ret.append(line)
            return ret

        return []
    except:
        return []

def parse_json_str(content):
    if content == "":
        content = "{}"

    return json.loads(content)

def json_stringify(json_ele):
    return json.dumps(json_ele)

# round off, millisecond, current time stamp.
def current_time():
    return int(time.time() * 1000 + 0.5)

def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def script_dir():
    return os.path.dirname(sys.argv[0])

def load_json_from_file(fname):
    try:
        with open(fname, "r") as f:
            return json.load(f)
    except:
        return None

def write_json_to_file(fname, json_ele):
    json_str = json_stringify(json_ele)
    with open(fname, "w") as f:
        f.write(json_str)

def ensure_dir(path):
    try:
        os.makedirs(path)
    except:
        pass

def dict_deep_copy(d):
    return copy.deepcopy(d)

def getLiDetail(node,keyword,bIndex = 5,eIndex = None):
    result = node.find(text=re.compile(keyword))
    result = result.parent.parent.text[bIndex:eIndex] if result != None else '未知'
    return result
