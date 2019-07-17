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
        
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH]
        adjLow = needData[t.LOW]
        adjOpen = needData[t.OPEN]
        adjReturn = needData[t.PCTCHG]
#        ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 -Ts_Rank(returns, 32)))
        
        x_1 = self.calculator.Corr(self.calculator.Delay(adjClose-adjOpen,1),adjClose,15)
        x_2 =  self.calculator.Rank(adjOpen - adjClose)
        x_3 = self.calculator.Rank(Volume/self.calculator.Delay(Volume,1))
        factor = self.calculator.Mean(self.calculator.Rank(x_1) + x_2+x_3,3)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()