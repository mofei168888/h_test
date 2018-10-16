#!/usr/bin/env python
# -*- coding: utf-8 -*-


from core.huobi.Huobi_Services import *

if __name__ == '__main__':
    hs = HuobiServices()
    ts = hs.get_depth('xrpusdt')
    print(ts)



