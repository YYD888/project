#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:30:55 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 09:20:05 2019

@author: yanyadong
"""


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
                           t.MKTCAP,t.MKTCAPFL,t.BUY_VALUE_LARGE_ORDER]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]
        adjReturn = needData[t.PCTCHG]
        BUY_VALUE_LARGE_ORDER =needData[t.BUY_VALUE_LARGE_ORDER]
#        TOT_VOLUME_BID = needData[t.TOT_VOLUME_BID]
        adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        
#        x_1 = (self.calculator.Decaylinear(self.calculator.Delay(adjHigh,1),5))
        x_2 = self.calculator.Rank(adjReturn)
        x_3 = self.calculator.Corr((adjVwap*0.7+0.3*adjLow),(BUY_VALUE_LARGE_ORDER),8)
#        x_4 = -(self.calculator.Rank(x_3-self.calculator.Delay(x_3,11)))
#        x_5 = self.calculator.Rank(x_3)
#     
        factor = self.calculator.Sma(self.calculator.Delay(-x_2*x_3,4),8,3)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()