#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 09:23:15 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:26:12 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:43:22 2019

@author: yanyadong
"""


# coding=utf8
__author__ = 'wangjp'

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
        self.needFields = [t.OPEN,t.BUY_VALUE_LARGE_ORDER,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,
                           t.HIGH,t.LOW,t.PCTCHG,t.MKTCAP,t.PSTTM, t.HIGH,t.PETTM,
                           t.OPEN_NET_INFLOW_RATE_VALUE,t.S_MFD_INFLOW_CLOSE,t.NET_INFLOW_RATE_VALUE,t.MKTCAPFL]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
#        S_MFD_INFLOW_CLOSE = needData[t.S_MFD_INFLOW_CLOSE] * needData[t.ADJFCT]
        adjClose = needData[t.CLOSE]  *needData[t.ADJFCT]
#        OPEN_NET_INFLOW_RATE_VALUE = needData[t.OPEN_NET_INFLOW_RATE_VALUE] * needData[t.ADJFCT]
        PSTTM = needData[t.PSTTM] *needData[t.ADJFCT]
        PETTM = needData[t.PETTM] *needData[t.ADJFCT]
        adjHigh =  needData[t.HIGH] *needData[t.ADJFCT]
        Volume = needData[t.VOLUME]

#        NET_INFLOW_RATE_VALUE =  needData[t.NET_INFLOW_RATE_VALUE]* needData[t.NET_INFLOW_RATE_VALUE]
#        adjLow =  needData[t.LOW]* needData[t.ADJFCT]
#        BUY_VALUE_LARGE_ORDER  = needData[t.BUY_VALUE_LARGE_ORDER]#DAHU
        
        x_1 = self.calculator.Corr(self.calculator.Rank(adjHigh),self.calculator.Rank(Volume),5)
        x_2 = self.calculator.Sum(x_1,5)
#        x_3 = self.calculator.Corr(self.calculator.Rank(x_1),self.calculator.Rank(x_2),30)    
#        x_4 = self.calculator.Rank(x_3)
#        x_5 =  x_4-self.calculator.Rank(adjClose/self.calculator.Delay(adjClose,1))
        factor = self.calculator.Rank(-x_2)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()