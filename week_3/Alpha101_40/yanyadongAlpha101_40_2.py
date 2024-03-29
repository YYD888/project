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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.TRDSTAT, t.SHRFREE,]  # 设置需要的字段

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
        adjHigh = needData[t.HIGH]
        adjLow = needData[t.LOW]
        adjOpen = needData[t.OPEN]
        adjReturn = needData[t.PCTCHG]
        
        x_1 = -1 * self.calculator.FindRank(self.calculator.Std(adjHigh,15),10)
        x_2 = -1 * self.calculator.FindRank(self.calculator.Std(adjClose,15),10)
        x_3 = -1 * self.calculator.Rank(self.calculator.Std(adjOpen,15))
        x_4 = self.calculator.Corr(adjHigh, Volume,6)
       
        
        factor = self.calculator.Wma(- x_4,7,0.4)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()