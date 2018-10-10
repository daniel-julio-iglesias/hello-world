#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
import json
import requests


# proxies = {
#     'http': 'http://username:password@Proxyadresse:Proxyport',
#     'https': 'https://username:password@Proxyadresse:Proxyport',
# }


class APITest:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_uri = 'http://httpbin.org'

    def get(self):
        uri = self.base_uri + '/get'
        print(uri)
        r = requests.get(self.base_uri + '/get')
        # r = requests.get(self.base_uri + '/get', proxies=proxies)
        return r.json()


def main():
    # print("Hello World!")
    api_test = APITest()
    print(api_test.get())

    # r = requests.get('http://httpbin.org/get', proxies=proxies)
    # print(r)


if __name__ == '__main__':
    main()
