#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 09:10:51 2019

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
        self.needFields = [t.CLOSE,t.OPEN,t.TURN,t.VOLUME, t.LOW, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.PDD,
                           t.BUY_VOLUME_EXLARGE_ORDER,t.MKTCAP,t.SHRFREE,t.VWAP]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        

        adjClose = needData[t.CLOSE] * needData[t.ADJFCT]
        adjHigh = needData[t.HIGH] * needData[t.ADJFCT]
        adjLow =  needData[t.LOW] * needData[t.ADJFCT]
        adjvolume = needData[t.VOLUME]* needData[t.ADJFCT]
        
        
        x_1 = self.calculator.Corr(self.calculator.Mean(adjvolume,17),adjLow,11)
        x_2 = (1.01*adjHigh+adjLow)/2
        x_3 =self.calculator.Rank(x_1+ x_2 - adjClose)
     
        
        factor = self.calculator.Wma(x_3,5,0.5)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()