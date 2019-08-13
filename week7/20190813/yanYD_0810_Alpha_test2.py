

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 12:00:28 2019

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
        self.neutral =True
        self.factorName = __name__.split('.')[-1]
        self.needFields = [t.OPEN,t.BUY_VALUE_LARGE_ORDER,t.VWAP,t.CLOSE,t.VOLUME, t.ADJFCT, t.TRDSTAT,t.HIGH,t.LOW,t.PCTCHG,
                           t.MKTCAP,t.MKTCAPFL,t.SHRFREE, t.HIGH,t.BUY_TRADES_EXLARGE_ORDER]  # 设置需要的字段

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
        BUY_TRADES_EXLARGE_ORDER =needData[t.BUY_TRADES_EXLARGE_ORDER]
        SHRFREE = needData[t.SHRFREE] * needData[t.ADJFCT]
        adjOpen =  needData[t.OPEN]* needData[t.ADJFCT]
        adjHigh =  needData[t.HIGH]* needData[t.ADJFCT]
        adjLow =  needData[t.LOW]* needData[t.ADJFCT]
         
         
        x_1 = self.calculator.FindRank((BUY_TRADES_EXLARGE_ORDER),30)
        x_2 = self.calculator.FindRank(adjVwap,4)
        x_3 = self.calculator.FindRank(Volume,5)
#        x_4 = self.calculator.Rank(Volume)
#        x_5 =(self.calculator.Delay(x_1,15)+x_2)/self.calculator.Delay(x_3,5)
#        x_6 =abs(self.calculator.RegResi(np.log(needData[t.MKTCAP]),x_5,15))
#        x = self.calculator.Sum(x=needData[t.VOLUME], num=10) / self.calculator.Sum(x=needData[t.SHRFREE], num=20)
#        x_7 = -(self.calculator.RegResi(x_6,x,15))
#        x_8 =self.calculator.Delay(x_7,4)
#        x_9 =self.calculator.Sma(x_8,10,6)
        factor =self.calculator.Wma(( x_1+x_2)*x_3,10,0.68)
        print('factor {0} done with {1} seconds'.format(self.factorName, time.time() - s))
        return factor

    def run_factor(self):
        self.run()
        



fct = Factor()
fct.run_factor()