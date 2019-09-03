#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:52:56 2019

@author: yanyadong
"""


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
                           t.MKTCAP,t.MKTCAPFL,t.CLOSE_NET_INFLOW_RATE_VALUE]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        adjHIGH = needData[t.HIGH] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]
        adjHigh = needData[t.HIGH]* needData[t.ADJFCT]
        CLOSE_NET_INFLOW_RATE_VALUE =needData[t.CLOSE_NET_INFLOW_RATE_VALUE]
#        TOT_VOLUME_BID = needData[t.TOT_VOLUME_BID]
        adjOpen = needData[t.OPEN] * needData[t.ADJFCT]
        
        x_1 = (adjClose<self.calculator.Delay(adjClose,1))*0+(adjClose>=self.calculator.Delay(adjClose,1))*CLOSE_NET_INFLOW_RATE_VALUE
        x_2 = self.calculator.RegResi(self.calculator.Mean(x=needData[t.PCTCHG], num=5),-x_1,165)
        x_3 = self.calculator.Wma(x_2,10,0.8)- self.calculator.Delay(x_2,2)*0.3
#        x_4 = -(self.calculator.Rank(x_3-self.calculator.Delay(x_3,11)))
#        x_5 = self.calculator.RegResi( self.calculator.Mean(x=needData[t.PCTCHG], num=5),self.calculator.Delay(S_MFD_INFLOWVOLUME,2),30)
#     
        factor =x_3
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()