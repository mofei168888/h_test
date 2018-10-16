#!/usr/bin/env python
# -*- coding: utf-8 -*-

from huobi.Huobi_Services import HuobiServices

if __name__ == '__main__':
    hs = HuobiServices()

    ts = hs.get_kline('xrpusdt','1day',size=1)
    print('high:%0.4f,low:%0.4f'%(ts['data'][0]['high'],ts['data'][0]['low']))

    td =hs.get_depth('xrpusdt')

    print('mid:%0.4f'%(float(ts['data'][0]['high'])+float(ts['data'][0]['low']))/2)

    print(td['tick']['bids'][0][0])
    print(td['tick']['asks'][0][0])

    print((td['tick']['bids'][0][0]+td['tick']['asks'][0][0])/2)