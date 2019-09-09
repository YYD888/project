
"""
Created on Mon Jul  8 23:10:58 2019

@author: YYD
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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH]
        adjLow = needData[t.LOW]
        
        x_1 = (adjHigh - self.calculator.Mean(adjClose,15))/self.calculator.Mean(adjClose,15)
        x_2 = self.calculator.Delay(x_1,3)
        x_4 =  self.calculator.Sma(x_1-x_2,7,2)
        x_5 = self.calculator.FindRank(x_4/self.calculator.Std(adjClose,14),16)
#        decay_wight =np.arange(1,6)/np.sum(np.arange(1,6))
        x_6 =self.calculator.FindRank(self.calculator.Sma(Volume,15,3)/self.calculator.Std(Volume,14),16) +x_5
        factor = self.calculator.Wma(x_6,5,0.2)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()