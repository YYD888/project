#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:51:05 2019

@author: yanyadong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 08:55:49 2019

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
        self.needFields = [t.CLOSE,t.OPEN,t.TURN,t.VOLUME, t.PE, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.PDD,
                           t.BUY_VOLUME_EXLARGE_ORDER,t.MKTCAP,t.SHRFREE,t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
#        adjVwap = needData[t.VWAP] * needData[t.ADJFCT]
        BUY_ORDER = needData[t.BUY_VOLUME_EXLARGE_ORDER] 
        PDD =  needData[t.PDD] 
        TURN= needData[t.TURN]
        adjClose = needData[t.CLOSE]* needData[t.ADJFCT]
        adjPE = needData[t.PE] *  needData[t.ADJFCT]
        adjVwap = needData[t.VWAP]
        
        x_1 = self.calculator.RegResi(adjClose/self.calculator.Delay(adjClose,1) -1,BUY_ORDER,18)
        x_2 = self.calculator.RegResi(TURN,adjClose/self.calculator.Delay(adjClose,1) -1,18)
#        liquidity20 =self.calculator.Std(x=needData[t.PCTCHG], num=5)
#        x_3  = ( -1+ self.calculator.Rank(self.calculator.Sum(-(4*x_1+2*x_2)*adjPE,20)))
        x_3 = self.calculator.Rank(self.calculator.Wma(3*x_1 +2*x_2,6,0.5))
        
        factor = self.calculator.Wma(x_3,5,0.5)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()