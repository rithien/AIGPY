#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   progressHelper.py
@Time    :   2018/12/28
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Show ProgressBar
'''

import sys
import time
import threading

class ProgressTool(object):
    def __init__(self, maxCount, barLength=50, icon='▓'):
        self.curCount  = 0                  #当前计数
        self.maxCount  = maxCount           #最大数量
        self.barLength = barLength          #进度条长度
        self.icon      = icon               #进度符号
        self.mutex     = threading.Lock()   #互斥锁

    def reset(self, maxCount):
        if self.mutex.acquire():
            self.curCount = 0  
            self.maxCount = maxCount  
            self.mutex.release()

    def setCurCount(self, curCount):
        if self.mutex.acquire():
            if curCount >= self.maxCount:
                curCount = self.maxCount
            self.curCount = self.maxCount
            self._show()
            self.mutex.release()

    def step(self):
        if self.mutex.acquire():
            if self.curCount >= self.maxCount:
                return
            self.curCount += 1
            self._show()
            self.mutex.release()

    def _show(self):
        #计算显示几个进度块
        numBlock = int(self.curCount * self.barLength / self.maxCount)  # 计算显示多少个'>'
        #计算显示几个空格
        numEmpty = self.barLength - numBlock
        #计算百分比
        percent = self.curCount * 100.0 / self.maxCount  
        #输出字符串
        process = '%3d' % percent + '%|' + self.icon*numBlock + ' '*numEmpty + '| ' + str(self.curCount) + '/' + str(self.maxCount) 
        #判断是否要换行
        if self.curCount < self.maxCount:
            process += '\r'
        else:
            process += '\n'
            
        sys.stdout.write(process)  
        sys.stdout.flush()

