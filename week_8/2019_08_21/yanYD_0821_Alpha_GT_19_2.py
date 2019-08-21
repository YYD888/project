

import time

import numpy as np
import pandas as pd
from FactorModule.FactorBase import FactorBase
from DataReaderModule.Constants import ALIAS_FIELDS as t

class Factor(FactorBase):

    def __init__(self):
        super(Factor,self).__init__()
        self.neutral = True
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.OPEN,t.BUY_VALUE_LARGE_ORDER,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,
                           t.MKTCAP,t.MKTCAPFL,t.PE,t.ADJCLOSE,t.SELL_TRADES_EXLARGE_ORDER,t.BUY_VOLUME_LARGE_ORDER]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVWAP = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        HIGH = needData[t.HIGH] * needData[t.ADJFCT]
        CLOSE= needData[t.CLOSE] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]* needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]
        SELL_TRADES_EXLARGE_ORDER =needData[t.SELL_TRADES_EXLARGE_ORDER]
        BUY_VOLUME_LARGE_ORDER = needData[t.BUY_VOLUME_LARGE_ORDER]
        PE = needData[t.PE] * needData[t.ADJFCT]
        
        
        x_1 = self.calculator.Rank(SELL_TRADES_EXLARGE_ORDER)
        x_2 = self.calculator.Rank(BUY_VOLUME_LARGE_ORDER)
        x_3 = (CLOSE>self.calculator.Delay(self.calculator.Mean(CLOSE,15),1))*x_2 + (CLOSE<=self.calculator.Delay(self.calculator.Mean(CLOSE,15),1))*0
        x_4 =x_3- self.calculator.Wma(self.calculator.Delay(x_3,1),8,0.5)*0.5
        x_5 = self.calculator.RegResi(self.calculator.Mean(x=needData[t.PCTCHG], num=5),x_4,15)
        factor =self.calculator.Rank(self.calculator.Decaylinear(x_5,5))
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()