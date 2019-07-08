 
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
        self.needFields = [t.HIGH, t.LOW, t.VOLUME, t.ADJFCT, t.VWAP,t.ADJCLOSE,t.TURN, t.PE,t.OPEN]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数据
         
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjLow = needData[t.LOW] * needData[t.ADJFCT]
        Volume= needData[t.VOLUME]
        adjClose = needData[t.ADJCLOSE]
        adjTURNTURN = needData[t.TURN]
        adjPe = needData[t.PE]
        adjOpen = needData[t.OPEN]
        
        x_1 = self.calculator.Mean((adjHigh - adjLow)/Volume + adjTURNTURN,7)
        x_2 = self.calculator.Mean(((adjHigh - adjLow)/2 - (self.calculator.Delay(adjHigh,num=1) + self.calculator.Delay(adjLow,num=1))/2),7)
        x_3 = self.calculator.Mean((self.calculator.Delay(adjPe,1)-self.calculator.Delay(adjPe,2))/self.calculator.Delay(adjPe,2),7)
        x_4 = self.calculator.Mean((adjClose - adjOpen)/adjClose,7)
        distrib = self.calculator.Sma(x_1*2+x_2*2+x_3+x_4,7,2)/self.calculator.Std(adjClose,7)
        factor =   distrib
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()



fct = Factor()
fct.run_factor()

