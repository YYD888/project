#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:17:32 2019

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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,t.MKTCAP]  # 设置需要的字段

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
        
        
        
        x_1 = (self.calculator.Delay(adjClose,3)-adjClose)/3
        x_2 = (self.calculator.Delay(Volume,3)-Volume)/3
        x_3 =(self.calculator.Delay(adjHigh,3)-adjHigh)/3
        x_4 = self.calculator.Rank(-(x_3+x_2+x_1))
        x_5 =  self.calculator.Wma(x_4,7,0.85)
     
        factor = x_5
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()