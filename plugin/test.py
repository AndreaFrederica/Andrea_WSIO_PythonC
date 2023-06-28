import module
from module import log

from module.register import initRegister, timerBasicRegister

@initRegister
def init():
    log.info("plugin \"test\" loaded")

@timerBasicRegister(time_sec= 10, type="cycle", cycles=-1)
def timerFunc():
    log.success("test")

@timerBasicRegister(time_sec=5,type="normal")
def test():
    log.success("只会执行一次")