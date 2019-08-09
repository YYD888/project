#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 09:40:45 2019

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
                           t.MKTCAP,t.MKTCAPFL,t.SHRFREE, t.HIGH]  # 设置需要的字段

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
        BUY_VALUE_LARGE_ORDER =needData[t.BUY_VALUE_LARGE_ORDER]
        SHRFREE = needData[t.SHRFREE] * needData[t.ADJFCT]
        adjOpen =  needData[t.OPEN]* needData[t.ADJFCT]
        adjHigh =  needData[t.HIGH]* needData[t.ADJFCT]
        adjLow =  needData[t.LOW]* needData[t.ADJFCT]
         
         
        x_1 = self.calculator.Sum(self.calculator.Std(adjVwap,20),22)
        x_2 = self.calculator.Corr(adjVwap,x_1,10)
        x_3 = self.calculator.Rank(x_2)
        x_4 = self.calculator.Rank(self.calculator.Rank(adjOpen)*2)
        x_5 = self.calculator.Rank((adjHigh + adjLow)/2)  + self.calculator.Rank(adjHigh)
        x_6 = (x_3/x_5)
        x_7 = -self.calculator.Delay(-(x_6-(self.calculator.RegResi( np.log(needData[t.MKTCAP]), x_4,10))),2)
        factor = self.calculator.Wma(x_7,7,0.55)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()