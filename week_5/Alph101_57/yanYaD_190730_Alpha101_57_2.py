#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 08:58:57 2019

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
        self.needFields = [t.OPEN,t.VWAP,t.CLOSE,t.TURN,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.PCTCHG,t.MKTCAP,t.MKTCAPFL]  # 设置需要的字段

    def factor_definition(self):
        """a
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVwap = needData[t.VWAP]*needData[t.ADJFCT]
        adjClose = needData[t.CLOSE]*needData[t.ADJFCT]
        adjHigh = needData[t.HIGH]*needData[t.ADJFCT]
      
        x_1 =  (adjClose) -adjVwap
        x_2 = self.calculator.Rank(self.calculator.Max( adjClose,6))
        x_3 = self.calculator.Decaylinear(x_2,3)
        momentum5 = self.calculator.Mean(x=needData[t.PCTCHG], num=5)
        x_4 =self.calculator.Wma( self.calculator.Wma(-x_1/x_3,10,0.5),6,0.6)
        x_5 = self.calculator.RegResi(momentum5,x_4,12)
        factor = self.calculator.Wma(x_5,7,0.5)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()