 
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
        self.needFields = [t.HIGH, t.LOW, t.VOLUME, t.ADJFCT, t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据
         
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        Vwap= needData[t.VWAP]
        
        x_1 = ((adjHigh +  adjLow)/2)*4+ (Vwap * 0.1)
        distrib = self.calculator.Rank(self.calculator.Delay(x_1,num=4)*-1)
        factor =   distrib
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()

