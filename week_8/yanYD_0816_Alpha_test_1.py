#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 15:10:03 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:35:42 2019

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
                           t.SHRFREE,t.S_MFD_INFLOW_CLOSE,t.NET_INFLOW_RATE_VALUE,t.MKTCAPFL]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        
        adjClose =  needData[t.CLOSE]* needData[t.ADJFCT]
        MKTCAPFL = needData[t.MKTCAPFL]*needData[t.ADJFCT]
        Volume =  needData[t.VOLUME]
        SHRFREE = needData[t.SHRFREE]*needData[t.ADJFCT]
        
        x_1 = (MKTCAPFL-self.calculator.Delay(MKTCAPFL,15) )/self.calculator.Delay(MKTCAPFL,15) 
        x_2 = self.calculator.Rank(-x_1)
        x_3 = self.calculator.Rank(Volume- self.calculator.Delay(Volume,15)/self.calculator.Delay(Volume,15))
        x_4 = self.calculator.RegResi(x_2,x_3,50)
        x_5 = x_4- self. calculator.Delay(x_4,1)*0.9
        x_6 = self.calculator.Sma(x_5,12,0.6)
        x_7 =x_6 -self.calculator.Delay(x_6,1)
        x_8 =self.calculator.Wma(x_7,10,0.9)
        factor = self.calculator.Wma(x_8,5,0.3)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()