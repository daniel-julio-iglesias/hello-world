#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Sample Configuration File
"""

import os


class Config:
    def __init__(self):
        # You can get an API key for free at 1forge.com
        self.FORGE_API_KEY = os.environ.get('FORGE_API_KEY') or 'YOUR_API_KEY'

        # In case you receive an Error Message as
        # "(...)IOError: [Errno socket error] [Errno 10060] A connection attempt failed because the
        # connected party did not properly respond after a period of time, or established connection
        # failed because connected host has failed to respond (...)"
        # and you are behind a proxy
        # adapt the next environment variables
        # os.environ['http_proxy'] = 'http://username:password@Proxyadresse:Proxyport'
        # os.environ['https_proxy'] = 'https://username:password@Proxyadresse:Proxyport'


if __name__ == '__main__':
    config = Config()
    # print("FORGE_API_KEY: {}".format(config.FORGE_API_KEY))
