#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:38:01 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:03:23 2019

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
        self.needFields = [t.OPEN,t.BUY_VALUE_LARGE_ORDER,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,
                           t.MKTCAP,t.MKTCAPFL,t.SHRFREE, t.HIGH,t.BUY_VALUE_MED_ORDER,t.MKTCAPFL]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]
        adjReturn = needData[t.PCTCHG]
        BUY_VALUE_MED_ORDER = needData[t.BUY_VALUE_MED_ORDER]
        BUY_VALUE_LARGE_ORDER =needData[t.BUY_VALUE_LARGE_ORDER]
        SHRFREE = needData[t.SHRFREE] * needData[t.ADJFCT]
        adjOpen =  needData[t.OPEN]* needData[t.ADJFCT]
        adjHigh =  needData[t.HIGH]* needData[t.ADJFCT]
        adjLow =  needData[t.LOW]* needData[t.ADJFCT]
        MKTCAPFL = needData[t.MKTCAPFL]
         
        x_1 = (BUY_VALUE_MED_ORDER +BUY_VALUE_LARGE_ORDER)/2 -(self.calculator.Delay(BUY_VALUE_MED_ORDER,4) +self.calculator.Delay(BUY_VALUE_LARGE_ORDER,4))/2
        x_2 = (adjHigh +adjLow)/2 -(self.calculator.Delay(adjHigh,4) +self.calculator.Delay(adjLow,4))/2
        x_3 =x_2*x_1/MKTCAPFL
        x_4 =  -self.calculator.Rank(x_3)
#        x_5 = (self.calculator.Delay(x_4,3))
#        x_6 =self.calculator.RegResi(self.calculator.Mean(x=needData[t.PCTCHG], num=15),x_5,5)
        factor =self.calculator.Wma(x_4,7,0.58)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()