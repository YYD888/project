#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 08:59:33 2019

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
                           t.HIGH,t.LOW,t.PCTCHG,t.MKTCAP,t.MKTCAPFL,t.SHRFREE, t.HIGH,t.BUY_VALUE_MED_ORDER,
                           t.BUY_VALUE_SMALL_ORDER,t.BUY_VALUE_LARGE_ORDER,t.BUY_VALUE_EXLARGE_ORDER]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
#        Volume = needData[t.VOLUME] 
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
#        adjMktcapfl = needData[t.MKTCAPFL]
#        adjReturn = needData[t.PCTCHG]
#        BUY_VALUE_EXLARGE_ORDER =needData[t.BUY_VALUE_EXLARGE_ORDER] #jigou
#        BUY_VALUE_SMALL_ORDER = needData[t.BUY_VALUE_SMALL_ORDER] #SANHU
#        adjOpen =  needData[t.OPEN]* needData[t.ADJFCT]
        adjHigh =  needData[t.HIGH]* needData[t.ADJFCT]
        adjLow =  needData[t.LOW]* needData[t.ADJFCT]
#        BUY_VALUE_LARGE_ORDER = needData[t.BUY_VALUE_LARGE_ORDER]#DAHU
        
        x_1 = self.calculator.Rank((adjHigh - self.calculator.Sum(adjVwap,8)/8))
        x_2 = self.calculator.Rank(np.abs((adjLow -adjVwap)))
        x_3 =self.calculator.Std(x=needData[t.PCTCHG], num=30)
        x_4 = self.calculator.RegResi(x_3,-x_1+x_2,30)
        
        factor = self.calculator.Wma(x_4,7,0.45)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()