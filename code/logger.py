from __future__ import unicode_literals
import logging
import sys
from singleton import Singleton

root='UnusualGUI'
level=logging.DEBUG
filename=None
logfrmt='%(levelname)s - %(asctime)s:%(msecs)d - %(name)s: %(message)s'

class Logger:
    __metaclass__=Singleton
    
    def __init__(self):
        self.loggers={}
        formatter=logging.Formatter(logfrmt,'%H:%M:%S')
        self.console = logging.StreamHandler(sys.stdout)
        self.console.setLevel(level)
        self.console.setFormatter(formatter)
        if filename is not None:
            self.filelogger=logging.FileHandler(FILENAMEHERE)
            self.filelogger.setFormatter(formatter)
    
    def get(self,subname):
        name='%s.%s' %(root,subname)
        if name in self.loggers: return self.loggers[name]
        l=logging.getLogger(name)
        l.handlers = []
        l.addHandler(self.console) 
        if filename is not None:
            l.addHandler(filelogger)
        l.setLevel(level)
        self.loggers[name]=l
        return l

logger=Logger()

def get(subname):
    return logger.get(subname)    
