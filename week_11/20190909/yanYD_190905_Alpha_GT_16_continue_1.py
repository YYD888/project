

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
        self.needFields = [t.OPEN,t.CLOSE_NET_INFLOW_RATE_VALUE,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,
                           t.MKTCAP,t.MKTCAPFL,t.PDD]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVWAP = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjHIGH= needData[t.HIGH] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]* needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]
        CLOSE_NET_INFLOW_RATE_VALUE =needData[t.CLOSE_NET_INFLOW_RATE_VALUE]
        PDD = needData[t.PDD] * needData[t.ADJFCT]
        
        
        x_1= -CLOSE_NET_INFLOW_RATE_VALUE

        
#        x_4 =  self.calculator.TsToMax(self.calculator.Rank(x_1),5)
#        x_5 = self.calculator.Corr(adjVWAP,BUY_VALUE_LARGE_ORDER/adjMktcapfl,10)
#        x_6  =self.calculator.TsToMax(self.calculator.Rank(x_5),5)
#        x_7 = self.calculator.Corr(Volume,BUY_VALUE_LARGE_ORDER/adjMktcapfl,10)
#        x_8 = self.calculator.TsToMax(self.calculator.Rank(x_7),5)
#        x_9 =  - (x_4+x_3+x_6+x_8)
#        x_10 = self.calculator.Delay(x_9,1)*0.2+ x_9-self.calculator.Delay(x_9,2)*0.3-self.calculator.Delay(x_9,4)*0.4 +self.calculator.Delay(x_9,5)*0.4
#        x_11 = self.calculator.Sma(x_10,6,2) 
        factor =self.calculator.Wma(x_1,10,0.7)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()