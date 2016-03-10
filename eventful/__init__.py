#!/usr/bin/env python

import os, sys

# Add root selenium test directory to system path if not already set
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from testconfig import config

TEST_ENV = config.get('TEST_ENV', 'dev')
TEST_URL = config.get('TEST_URL', None)
BROWSER = config.get('BROWSER', 'Chrome')

def get_url(json_url_data):
    if TEST_URL:
        return TEST_URL
    else:
        return json_url_data[TEST_ENV]