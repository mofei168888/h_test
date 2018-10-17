#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.huobi.Huobi_Services import *
from core.Logger import *

if __name__ == '__main__':
    hs = HuobiServices()
    result = hs.get_balance('935082')

    print('test go')
    for i in range(0, len(result['data']['list'])):
        if result['data']['list'][i]['currency'] == 'xrp':
            print(result['data']['list'][i])


