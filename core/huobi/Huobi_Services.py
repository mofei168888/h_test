#!/usr/bin/env python
# -*- coding: utf-8 -*-


from core.settings import *
from core.huobi.Huobi_Utils import *


class HuobiServices:

    def __init__(self):
        self.utils = Huobi_Utils('params.json')

    def get_accounts(self):
        """
        #获取账户信息
        :return:
        """
        path = '/v1/account/accounts'
        params = {}
        return self.utils.api_key_get(params,path)

    def get_balance(self,acct_id=None):
        """ #获取账户余额
        :param acct_id
        :return:
        """
        if not acct_id:
            accounts = self.get_accounts()
            acct_id = accounts['data'][0]['id']

        url = "/v1/account/accounts/{0}/balance".format(acct_id)
        params = {"account-id": acct_id}
        return self.utils.api_key_get(params, url)

    def get_depth(self,symbol,type='step0'):
        """#获取交易深度
        :param symbol
        :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        params = {'symbol': symbol,
                  'type': type}

        url = self.utils.params['URL']+'/market/depth'

        return self.utils.http_get_request(url, params)

    def get_kline(self,symbol,period,size=100):
        """ #获取交易K线
        :param symbol
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size: 可选值： [1,2000]
        :return:
        """
        params = {'symbol': symbol,
                  'period': period,
                  'size': size}

        url = self.utils.params['URL'] + '/market/history/kline'
        return self.utils.http_get_request(url, params)

    def get_trade_detail(self,symbol):
        """获取tradedetail
            :param symbol
            :return:
            """
        params = {'symbol': symbol}

        url = self.utils.params['URL'] + '/market/trade'
        return self.utils.http_get_request(url, params)

    def get_ticker(self,symbol):
        """获取merge ticker
        :param symbol:
        :return:
        """
        params = {'symbol': symbol}

        url = self.utils.params['URL'] + '/market/detail/merged'
        return self.utils.http_get_request(url, params)

    def get_trade_24qty(self,symbol):
        """获取 Market Detail 24小时成交量数据
        :param symbol
        :return:
        """
        params = {'symbol': symbol}

        url = self.utils.params['URL'] + '/market/detail'
        return self.utils.http_get_request(url, params)

    def get_symbols(self,long_polling=None):
        """获取  支持的交易对

        """
        params = {}
        if long_polling:
            params['long-polling'] = long_polling
        path = '/v1/common/symbols'
        return self.utils.api_key_get(params, path)

    def send_order(self,amount, source, symbol, _type, price=0):
        """ 创建并执行订单
         :param amount:
         :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
         :param symbol:
         :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
         :param price:
         :return:
         """
        if HUOBI_PARAMS['ACCOUNT_ID']:
            acct_id = HUOBI_PARAMS['ACCOUNT_ID']

        else:
            try:
                accounts = self.get_accounts()
                acct_id = accounts['data'][0]['id']
            except BaseException as e:
                print('get acct_id error.%s' % e)
                acct_id = HUOBI_PARAMS['ACCOUNT_ID']

        params = {"account-id": acct_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": source}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self.utils.api_key_post(params, url)

    def cancel_order(self,order_id):
        """
        # 撤销订单
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/submitcancel".format(order_id)
        return self.utils.api_key_post(params, url)

    def get_order_info(self,order_id):
        """
        查询某个订单
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}".format(order_id)
        return self.utils.api_key_get(params, url)

    def get_order_results(self,order_id):
        """
        # 查询某个订单的成交明细
        :param order_id:
        :return:
        """
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(order_id)
        return self.utils.api_key_get(params, url)

    def get_order_list(self,symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """
        #获取订单列表
        :param symbol:
        :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date:
        :param end_date:
        :param _from:
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol,
                  'states': states}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/orders'
        return self.utils.api_key_get(params, url)

    def get_orders_results(self,symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
        """
        # 查询当前成交、历史成交
        :param symbol:
        :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param start_date:
        :param end_date:
        :param _from:
        :param direct: 可选值{prev 向前，next 向后}
        :param size:
        :return:
        """
        params = {'symbol': symbol}

        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/matchresults'
        return self.utils.api_key_get(params, url)

    def withdraw(self, address, amount, currency, fee=0.0100, addr_tag=""):
        """
        # 申请提现虚拟币
        :param address_id:
        :param amount:
        :param currency:btc, ltc, bcc, eth, etc ...(火币Pro支持的币种)
        :param fee:
        :param addr-tag:  #仅XRP提币地址需要Tag
        :return: {
                   "status": "ok",
                   "data": 700
                 }
        """
        params = {'address': address,
                  'amount': amount,
                  "currency": currency,
                  "fee": fee,
                  "addr-tag": addr_tag}
        url = '/v1/dw/withdraw/api/create'
        return self.utils.api_key_post(params, url)

    def cancel_withdraw(self,address):
        """
         # 申请取消提现虚拟币
        :param address:
        :return: {
                  "status": "ok",
                  "data": 700
                }
        """
        params = {}
        url = '/v1/dw/withdraw-virtual/{0}/cancel'.format(address)

        return self.utils.api_key_post(params, url)

    def send_margin_order(self,amount,symbol, _type, source='margin',price=0):
        """
        # 创建并执行借贷订单
        :param amount:
        :param source: 'margin'
        :param symbol:
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        :param price:
        :return:
        """
        try:
             accounts = self.get_accounts()
             for account in accounts['data']:
                 if account['type'] == source and account['subtype']==symbol and account['state']=='working':
                    acct_id = account['id']

        except BaseException as e:
             print('get acct_id error.%s' % e)
             acct_id = ''

        params = {"account-id": acct_id,
                  "amount": amount,
                  "symbol": symbol,
                  "type": _type,
                  "source": 'margin-api'}
        if price:
            params["price"] = price

        url = '/v1/order/orders/place'
        return self.utils.api_key_post(params, url)

    def exchange_to_margin(self, symbol, currency, amount):
        """#将资金从现货账户转入借贷账户
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-in/margin"
        return self.utils.api_key_post(params, url)

    def margin_to_exchange(self,symbol, currency, amount):
        """# 将资金从借贷账户转入现货账户
         :param amount:
         :param currency:
         :param symbol:
         :return:
         """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}

        url = "/v1/dw/transfer-out/margin"
        return self.utils.api_key_post(params, url)

    def apply_margin(self,symbol, currency, amount):
        """    #申请借贷
        :param amount:
        :param currency:
        :param symbol:
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency,
                  "amount": amount}
        url = "/v1/margin/orders"
        return self.utils.api_key_post(params, url)

    def repay_margin(self,order_id, amount):
        """归还借贷
         :param order_id:
         :param amount:
         :return:
         """
        params = {"order-id": order_id,
                  "amount": amount}
        url = "/v1/margin/orders/{0}/repay".format(order_id)
        return self.utils.api_key_post(params, url)

    def get_loan_orders(self,symbol, currency, start_date="", end_date="", start="", direct="", size=""):
        """#获取借贷订单信息
        :param symbol:
        :param currency:
        :param direct: prev 向前，next 向后
        :return:
        """
        params = {"symbol": symbol,
                  "currency": currency}
        if start_date:
            params["start-date"] = start_date
        if end_date:
            params["end-date"] = end_date
        if start:
            params["from"] = start
        if direct and direct in ["prev", "next"]:
            params["direct"] = direct
        if size:
            params["size"] = size
        url = "/v1/margin/loan-orders"
        return self.utils.api_key_get(params, url)

    def get_margin_balance(self,symbol):
        """#获取借贷账户余额
           :param symbol:
           :return:
           """
        params = {}
        url = "/v1/margin/accounts/balance"
        if symbol:
            params['symbol'] = symbol

        return self.utils.api_key_get(params, url)


if __name__ == '__main__':
    hs = HuobiServices()

    '''#1. get_accounts  获取账户信息进行测试  
    result = hs.get_accounts()
    print(result)
    ''' #1 get_accounts  获取账户信息进行测试

    '''#2. get_balance  获取账户余额
    result = hs.get_balance('1021223')
    print(result)
    ''' #2.get_balance  获取账户余额

    result = hs.get_balance('935082')

    for i in range(0,len(result['data']['list'])):
        if result['data']['list'][i]['currency']=='xrp':
            print(result['data']['list'][i])

    '''#3.get_depth  获取交易深度
    result = hs.get_depth('ethusdt')
    print(result)
    '''#3.get_depth  获取交易深度


    '''#4.get_kline 获取K线数据
    result = hs.get_kline('ethusdt','1min')
    print(result)
    '''#4.get_kline 获取K线数据

    '''#5.get_trade_detail  获取交易数据
    result = hs.get_trade_detail('ethusdt')
    print(result)
    '''#5.get_trade_detail  获取交易数据

    '''#6.get_ticker 获取聚合行情
    result = hs.get_ticker('ethusdt')
    print(result)
    '''#6.get_ticker 获取聚合行情

    '''#7 get_trade_24qty 获取24小时成交数据
    result = hs.get_trade_24qty('ethusdt')
    print(result)
    '''#7 get_trade_24qty 获取24小时成交数据

    '''#8 get_symbols获取支持的交易对
    result = hs.get_symbols()
    print(result) 
    '''#8 get_symbols获取支持的交易对

    '''#9 send_order  发送订单
    result = hs.send_order(1, "", 'xrpusdt', ORDER_TYPE['SL'], 2.000)
    print(result)
    '''#9 send_order  发送订单

    '''#10.cancel_order  取消订单
    result = hs.cancel_order(781482417)
    print(result)
    '''#10.cancel_order  取消订单

    '''#11 get_order_info  获取订单详情
    result = hs.get_order_info('781482417')
    print(result)
    '''#11 get_order_info  获取订单详情

    '''#12 get_order_results 获取订单成交明细
    result = hs.get_order_results('792995310')
    print(result)
    '''#12 get_order_results 获取订单成交明细

    '''#13 get_order_list  获取订单列表
    result = hs.get_order_list('xrpusdt','submitted')
    print(result)
    for order in result['data']:
        res = hs.cancel_order(order['id'])
        print(res)
    '''#13 get_order_list  获取订单列表

    '''#14 get_orders_results 查询当前成交、历史成交
    result = hs.get_orders_results('xrpusdt')
    print(result)
    '''#14 get_orders_results 查询当前成交、历史成交

    '''#15 withdraw申请提币
    #result = hs.withdraw('0xecae55307a0e5c855d518dc3c2065f733fd0b6bc',8.76,'eth',fee=0.01)
    #print(result)
    '''#15 withdraw申请提币

    ''' #16 cancel_withdraw 取消
    result = hs.cancel_withdraw()
    print(result)
    '''#16 cancel_withdraw 取消

    '''#17 exchange_to_margin 将资金转到
    result = hs.exchange_to_margin('xrpusdt', 'xrp', 1)
    result = hs.exchange_to_margin('xrpusdt','xrp',3)
    print(result)
    '''#17 exchange_to_margin 将资金转到

    '''#18 get_margin_balance获取借贷账户资金余额
    result = hs.get_margin_balance获取借贷账户资金余额('xrpusdt')
    print(result['data'][0]['list'])
    '''#18 get_margin_balance获取借贷账户资金余额

    '''#19 send_margin_order  下借贷账户交易订单
    result = hs.send_margin_order(1,'xrpusdt',ORDER_TYPE['SL'],price=2.000)
    print(result)
    '''#19 send_margin_order  下借贷账户交易订单

    '''#20 margin_to_exchange  将资金从借贷账户转入现货帐户
    result = hs.margin_to_exchange('xrpusdt','xrp',1)
    print(result)
    '''#20 margin_to_exchange  将资金从借贷账户转入现货帐户

    '''#21 apply_margin 申请借贷
    result = hs.apply_margin('xrpusdt','usdt',2)
    print(result)
    '''#21 apply_margin 申请借贷

    '''#22 get_loan_orders获取借贷订单
    result = hs.get_loan_orders获取借贷订单('xrpusdt','usdt')
    print(result)
    '''#22 get_loan_orders获取借贷订单

    '''#23 repay_margin 归还借贷
    result = hs.repay_margin('',10)
    print(result)
    '''#23 repay_margin 归还借贷


