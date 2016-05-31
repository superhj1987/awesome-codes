#coding:utf-8

import common

LOG_DIR = common.script_dir() + '/logs/'
LOG_PATH = LOG_DIR + 'spider.log'
ERROR_PATH = LOG_DIR + 'spider_error.log'

common.ensure_dir(LOG_DIR)

def log(c):
    print c
    common.append_file(LOG_PATH,'\n[' + common.now_time() + ']' + str(c) + '\n')

def error(e):
    print e
    common.append_file(ERROR_PATH,'\n[' + common.now_time() + ']' + str(e) + '\n')
