#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ok.OK_Services import *



if __name__ == '__main__':
    ok = Ok_Services()
    i=0
    while i < 1:
        #i=i+1
        try:
            result = ok.get_future_depth('eth_usdt')
            sell = result['asks'][-5]  #卖出价格
            buy = result['bids'][0]  #买入价格
        #print(result['asks'][-3])
        #print(result['bids'][2])
        except Exception as e:
            print('error:%s'%e)
        finally:

            if sell[0]-buy[0] >2:
                print('sell:%s,buy:%s'%(sell,buy))

