#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests
import platform

from core.settings import *
from core.Logger import *

class Huobi_Utils:
    def __init__(self,params_file):
        self._platform = platform.system()  # Get platform type
        # Windows will be : Windows
        # Linux will be : Linux
        file_name = ""
        if self._platform == 'Windows':
            self._file_path = "D:\config"
            file_name = self._file_path + "\{}".format(params_file)
        elif self._platform == 'Linux':
            self._file_path = "/home"
            file_name = self._file_path + "/{}".format(params_file)
            # file_name = "/home/{}".format(params_file)
        with open(file_name, 'r') as fr:
            self.params = json.load(fr)

        #print(self.params)

    def http_get_request(self,url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }

        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)

        try:
            response = requests.get(url,postdata,headers=headers,timeout = 20)

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return None

    def http_post_request(self,url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)

        try:
            response = requests.post(url, postdata, headers=headers, timeout=20)  #
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except BaseException as e:
            print("httpPost failed, detail is:%s" % e)
            return None

    def create_sign(self,params, method, host_url, request_path, secret_key):
        sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    def api_key_get(self,params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.params['ACCESS_KEY'],
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = self.params['URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = self.create_sign(params, method, host_name, request_path, self.params['SECRET_KEY'])

        url = host_url + request_path
        return self.http_get_request(url, params)

    def api_key_post(self,params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.params['ACCESS_KEY'],
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = self.params['URL']
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self.create_sign(params_to_sign, method, host_name, request_path, self.params['SECRET_KEY'])
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self.http_post_request(url, params)

if __name__ == '__main__':
    hs = Huobi_Utils('params.json')
    print('test')




