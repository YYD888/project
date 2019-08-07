#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 11:25:22 2019

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
        self.neutral = False
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
        x_2 = self.calculator.Delay(self.calculator.Mean(x_1 ,15),4)
        x_3 = (x_1>=x_2) *x_1
        x_4 =  self.calculator.Mean(x=needData[t.PCTCHG], num=5)
        x_5  = self.calculator.Mean(x=needData[t.PCTCHG], num=15)
        x_6 =(self.calculator.RegResi(x_4,x_3,17))
        x_7 = self.calculator.RegResi(x_5,x_6,70)
        factor = self.calculator.Sma(x_7,7,2)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()