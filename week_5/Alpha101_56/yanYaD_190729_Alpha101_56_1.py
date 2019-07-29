#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:50:30 2019

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
        
        adjMktcap = needData[t.MKTCAP]*needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]*needData[t.ADJFCT]
        adjTurn = needData[t.TURN] * needData[t.ADJFCT]
        adjVwap  = needData[t.VWAP]*needData[t.ADJFCT]

        x_1 =  self.calculator.FindRank(self.calculator.Sum(adjReturn,10)/self.calculator.Sum(self.calculator.Sum(adjReturn,2),3),1)
        x_2 = self.calculator.FindRank(adjReturn* np.log(adjMktcap),3)

        factor = self.calculator.Wma(self.calculator.Wma(- x_1*x_2,5,0.98),5,0.4)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()