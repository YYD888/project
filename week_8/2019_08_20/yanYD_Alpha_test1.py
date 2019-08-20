#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 21:53:39 2019

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
        PDD =  needData[t.PDD]  *  needData[t.ADJFCT]
        TURN= needData[t.TURN] 
        adjClose = needData[t.CLOSE]* needData[t.ADJFCT]
        adjPE = needData[t.PE] *  needData[t.ADJFCT]
        adjOPEN = needData[t.OPEN] *  needData[t.ADJFCT]
        
        x_1 = (self.calculator.RegResi(adjClose/self.calculator.Delay(adjClose,1) -1,BUY_ORDER,20))
        x_2 = self.calculator.RegResi(TURN,adjClose/self.calculator.Delay(adjClose,1) -1,20)
#        liquidity20 =self.calculator.Std(x=needData[t.PCTCHG], num=5)
#        x_3  = ( -1+ self.calculator.Rank(self.calculator.Sum(-(4*x_1+2*x_2)*adjPE,20)))
        x_3 =(1*x_1 -6*x_2)
        x_4 = (self.calculator.RegResi(self.calculator.Mean(x=needData[t.PCTCHG], num=5),x_3,50))
        x_5 =self.calculator.Mean(x=needData[t.PCTCHG], num=15)
        x_6 =(self.calculator.RegResi(x_5, self.calculator.Sma(x_4,12,2), 14))
        factor = self.calculator.Sma(x_4,12,3)
        
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()