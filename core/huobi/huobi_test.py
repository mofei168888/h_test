#!/usr/bin/env python
# -*- coding: utf-8 -*-


from core.huobi.Huobi_Services import *

if __name__ == '__main__':
    hs = HuobiServices()
    hb_qty = []
    i = 0
    while i<1:
        try:
            price_hb = hs.get_depth('ethusdt', 'step0')
            hb_buy = price_hb['tick']['bids'][0][0]
            hb_sell = price_hb['tick']['asks'][0][0]
            hb_qty.append(price_hb['tick']['bids'][0][1])
            hb_qty.append(price_hb['tick']['asks'][0][1])

            qty = min(hb_qty)
        except Exception as e:
            print('error:%s' % e)

        finally:

            if hb_sell-hb_buy >1:
                print('火币买入价格：%s,火币卖出价格：%s,价格差异:%s,量：%s'%(hb_buy,hb_sell,hb_sell-hb_buy,qty))

                hb_buy = hb_buy +0.01
                hb_sell = hb_buy+0.5

                #print('buy:%s,sell:%s'%(hb_buy,hb_sell))
                order_buy = hs.send_order(0.01, "", 'ethusdt', ORDER_TYPE['BL'], hb_buy)
                order_sell = hs.send_order(0.01, "", 'ethusdt', ORDER_TYPE['SL'], hb_sell)

                #order_buy = hs.send_margin_order(0.1, 'margin', 'ethusdt', ORDER_TYPE['BL'], hb_buy)
                #order_sell =hs.send_margin_order(0.1, 'margin', 'ethusdt', ORDER_TYPE['SL'], hb_sell)

                print(order_buy)
                print(order_sell)