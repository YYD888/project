#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:06:39 2019

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
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH]* needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]
        BUY_VALUE_LARGE_ORDER =needData[t.BUY_VALUE_LARGE_ORDER]
        adjLow = needData[t.LOW]* needData[t.ADJFCT]
        adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        
        x_1 = ((self.calculator.Delay(adjHigh,3)-adjLow))
        x_2 = self.calculator.Max(adjHigh,3) +self.calculator.Max(adjLow,3)
        x_3 = x_1/x_2
        x_4 = self.calculator.RegResi( self.calculator.Mean(x=needData[t.PCTCHG], num=5),x_3,5)
#        x_5 = self.calculator.Rank(x_3)
#     
        factor =self.calculator.Delay(self.calculator.Wma(x_4,11,0.8),2)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()