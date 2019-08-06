#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:38:45 2019

@author: yanyadong
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:21:08 2019

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
        self.needFields = [t.CLOSE,t.OPEN,t.TURN,t.VOLUME, t.LOW, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.PCFOCF,
                           t.BUY_VOLUME_EXLARGE_ORDER,t.MKTCAP,t.SHRFREE,t.VWAP,t.NET_INFLOW_RATE_VOLUME_L,t.PCFOCFTTM]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
#        MAX(SUMAC(CLOSE-MEAN(CLOSE,24)))-MIN(SUMAC(CLOSE-MEAN(CLOSE,24)))/STD(CLOSE,24)

        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        PCFOCF =  needData[t.LOW] * needData[t.ADJFCT]
        adjOpen = needData[t.PCFOCF] * needData[t.ADJFCT]
        volume = needData[t.VOLUME]
        NET_INFLOW_RATE_VOLUME_L = needData[t.NET_INFLOW_RATE_VOLUME_L]
        PCFOCFTTM = needData[t.PCFOCFTTM]
        RETURN = needData[t.PCTCHG]
        
        
        
        x_1 = adjClose/self.calculator.Delay(adjClose,120) -1
#        print(x_1)
        x_2 = PCFOCFTTM/(self.calculator.Delay(PCFOCFTTM,120)) -1
#        print(x_2)

        x_3 =-(x_1>=0)*(x_2<=0)*self.calculator.Max(x_2,10) +(x_1<0)*(x_2<0)*self.calculator.Max(x_2,5)/6  \
                +(x_1>=0)*(x_2>=0)*self.calculator.Max(x_2,10)/2 +(x_1<0)*(x_2<0)/2+(x_1<0)*(x_2>=0)*self.calculator.Max(x_2,5)*2
        x_4 =-self.calculator.Rank(x_3)
        x_5 =x_4 +self.calculator.Rank(volume/self.calculator.Mean(volume,5))
        factor =self.calculator.Wma(x_5,3,0.3)
        
        
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()
