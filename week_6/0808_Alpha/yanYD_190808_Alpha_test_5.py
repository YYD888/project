#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 13:28:00 2019

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
        self.needFields = [t.OPEN,t.BUY_VALUE_LARGE_ORDER,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,
                           t.MKTCAP,t.MKTCAPFL,t.SHRFREE]  # 设置需要的字段

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
        adjMktcapfl = needData[t.MKTCAPFL]
        adjReturn = needData[t.PCTCHG]
        BUY_VALUE_LARGE_ORDER =needData[t.BUY_VALUE_LARGE_ORDER]
        SHRFREE = needData[t.SHRFREE] * needData[t.ADJFCT]
        
        x_1 = BUY_VALUE_LARGE_ORDER/SHRFREE
        x_2 = self.calculator.Rank(self.calculator.Max(x_1,8))
        x_3 = self.calculator.Rank(self.calculator.Delay(self.calculator.Max(np.log(Volume),5),1))
        x_4 = self.calculator.Corr(-x_2,x_3,13)
#        x_5 = self.calculator.Sum(x=needData[t.VOLUME], num=10) / self.calculator.Sum(x=needData[t.SHRFREE], num=10)
#        x_6 = x_4 - (self.calculator.RegResi(x_5,x_4,10))
       
        factor =self.calculator.Rank(x_4)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()