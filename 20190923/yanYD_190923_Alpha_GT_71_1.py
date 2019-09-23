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
        self.needFields = [t.OPEN,t.CLOSE_NET_INFLOW_RATE_VALUE,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.CLOSE_NET_INFLOW_RATE_VALUE,
                           t.MKTCAP,t.MKTCAPFL,t.SHRFREE,t.PDD,t.BUY_VOLUME_EXLARGE_ORDER,t.BUY_VOLUME_SMALL_ORDER,t.BUY_VOLUME_MED_ORDER]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        BUY_VOLUME_MED_ORDER= needData[t.BUY_VOLUME_MED_ORDER] 
        adjClose = needData[t.CLOSE]* needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]
        BUY_VOLUME_EXLARGE_ORDER =needData[t.BUY_VOLUME_EXLARGE_ORDER]
        BUY_VOLUME_SMALL_ORDER = needData[t.BUY_VOLUME_SMALL_ORDER]
        adjOpen = needData[t.OPEN]* needData[t.ADJFCT]
        adjLow = needData[t.LOW]* needData[t.ADJFCT]
        adjVwap = needData[t.VWAP] *needData[t.ADJFCT]
        CLOSE_NET_INFLOW_RATE_VALUE =needData[t.CLOSE_NET_INFLOW_RATE_VALUE]
        x_1 = self.calculator.Rank(CLOSE_NET_INFLOW_RATE_VALUE)
        x_2 =self.calculator.Rank((adjClose/self.calculator.Delay(adjClose,5))) 
        factor=-self.calculator.Sma(x_2+x_1,15,4)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        


fct = Factor()
fct.run_factor()