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
        self.neutral = False
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjOpen = needData[t.CLOSE] * needData[t.ADJFCT]
        
        x_1 = self.calculator.cmpMax((adjVwap-adjOpen*0.98),12)
        x_2 = self.calculator.cmpMin((adjVwap-adjOpen*0.98),12)
        x_3 = self.calculator.Delay(Volume,12)
#         self.calculator.Rank(x_2)
        distrib = self.calculator.Rank(x_1)  + self.calculator.Rank(x_3) + self.calculator.Rank(x_2)
        factor =  -distrib

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()