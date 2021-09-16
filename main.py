from __future__ import (absolute_import, division, print_function, unicode_literals)

import backtrader

# step1: MACD-黃金交叉和死亡交叉的判斷
class MACD(backtrader.Strategy):
   params = (('p1', 12), ('p2', 26), ('p3', 9),)  # 參數準則 - 可根據自行需求調整

   def __init__(self):
      self.order = None

      self.MACDhist = backtrader.indicators.MACDHisto(self.data,
                                                      period_me1=self.p.p1,
                                                      period_me2=self.p.p2,
                                                      period_signal=self.p.p3)

   def log(self, txt, dt=None):

      dt = dt or self.datas[0].datetime.date(0)
      print('%s, %s' % (dt.isoformat(), txt))

   def notify_order(self, order):
      if order.status in [order.Submitted, order.Accepted]:
         return

      if order.status in [order.Completed]:
         if order.isbuy():
            self.log("Buy Order executed; %s" % order.executed.price)
         elif order.issell():
            self.log("Sell Order executed; %s" % order.executed.price)

         self.bar_executed = len(self)

      self.order = None

   # 交易準則 - 當MACD柱>0(金叉)且沒有倉位時入場 = 買入點
   #           當MACD柱<0(死叉)且持有倉位時離場 = 賣出點
   def next(self):
      if not self.position:
         # 當前帳戶價值
         total_value = self.broker.getvalue()

         if self.MACDhist > 0:
            self.order = self.buy()
      else:
         if self.MACDhist < 0:
            self.close()

# step2 ： 模擬交易-加入參數、資料、策略。
def main():
   # 1.資金
   startcash = 100000
   # 2. 股票/虛擬貨幣的歷史數據
   data = backtrader.feeds.YahooFinanceCSVData(dataname = './Data/TSLA.csv')
   # 3. 初始化你的AI
   cerebro = backtrader.Cerebro()
   # 4. 加入歷史數據
   cerebro.adddata(data)
   # 5. 加入寫好的交易策略
   cerebro.addstrategy(MACD)
   # 6. 加入準備號的資金
   cerebro.broker.setcash(startcash)
   # 7.交易量
   cerebro.addsizer(backtrader.sizers.FixedSize, stake=100)
   # 8.手續費
   cerebro.broker.setcommission(commission=0.007)
   # 7. 開始交易
   cerebro.run()





   portvalue = cerebro.broker.getvalue()
   pnl = portvalue - startcash

   print('Final Portfolio Value: ${}'.format(portvalue))
   print('P/L: ${}'.format(pnl))

   cerebro.plot()








if __name__ == '__main__':
   main()


