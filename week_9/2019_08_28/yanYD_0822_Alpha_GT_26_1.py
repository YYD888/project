#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:59:46 2019

@author: yanyadong
"""



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
                           t.MKTCAP,t.MKTCAPFL,t.PE,t.ADJCLOSE,t.SELL_TRADES_EXLARGE_ORDER,t.BUY_VOLUME_LARGE_ORDER,t.SHRFREE]  # 设置需要的字段

    def factor_definition(self):
        """
        收集派发指标
        :return:
        """
        s = time.time()
        needData = self.needData                                # 计算所需数
        
        adjVWAP = needData[t.VWAP] * needData[t.ADJFCT]
        Volume = needData[t.VOLUME] 
        HIGH = needData[t.HIGH] * needData[t.ADJFCT]
        CLOSE= needData[t.CLOSE] * needData[t.ADJFCT]
        adjMktcapfl = needData[t.MKTCAPFL]* needData[t.ADJFCT]
        adjReturn = needData[t.PCTCHG]* needData[t.ADJFCT]
        SELL_TRADES_EXLARGE_ORDER =needData[t.SELL_TRADES_EXLARGE_ORDER]
        BUY_VOLUME_LARGE_ORDER = needData[t.BUY_VOLUME_LARGE_ORDER]
        PE = needData[t.PE] * needData[t.ADJFCT]
        
#        SMA((CLOSE<=DELAY(CLOSE,1)?STD(CLOSE,20):0),20,1))
    
        x_1 =  self.calculator.Sum(BUY_VOLUME_LARGE_ORDER,30)/30-BUY_VOLUME_LARGE_ORDER
        x_2 = self.calculator.Corr(adjVWAP,self.calculator.Delay(CLOSE,5),50)
        x_3 =-x_2*x_1
        x_4 =  self.calculator.RegResi(self.calculator.Mean(x=needData[t.PCTCHG], num=5),x_3,20)
        factor = self.calculator.Wma(x_4,10,0.6)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()