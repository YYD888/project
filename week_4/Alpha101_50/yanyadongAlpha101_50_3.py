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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.LOW,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.PCTCHG,t.MKTCAP,t.MKTCAPFL]  # 设置需要的字段

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
        adjLow = needData[t.LOW]
     
        
        x_1 = 1 * self.calculator.FindRank(adjClose/adjLow, 8)
        x_2 = x_1 +self.calculator.Delay(-1*x_1, 7)
        x_3 = self.calculator.Rank((self.calculator.Sum(adjReturn,15) -self.calculator.Sum(adjReturn, 30))/15)
        factor =  self.calculator.Wma(-x_2* x_3 *self.calculator.FindRank(Volume/self.calculator.Delay(Volume,1),12),10,0.85)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()