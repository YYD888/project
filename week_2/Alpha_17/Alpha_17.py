#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 15:34:07 2019

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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW]  # 设置需要的字段

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
        
        x_1 = self.calculator.Rank(adjVwap-self.calculator.Max(adjVwap,15))
        x_2 = self.calculator.Delay(adjClose,5)
#        distrib = self.calculator.Sum(x_2,6)
        factor =self.calculator.Sma(x_1+x_2,7,2)/self.calculator.Std(adjClose,7)

        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()
