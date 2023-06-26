import module

from module.register import initRegister, timerBasicRegister

@initRegister
def init():
    print("plugin \"test\" loaded")

@timerBasicRegister(time_sec= 10, type="cycle", cycles=-1)
def timerFunc():
    print("test")

@timerBasicRegister(time_sec=5,type="normal")
def test():
    print("只会执行一次")