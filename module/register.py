import asyncio
from functools import wraps
import functools
from importlib import import_module
import json
from typing import Any

import schedule
from module import tools
import config

from module import context
from module.log import info



async def taskRoute(command:object,session: object):
    #! command = String / Dict
    if(type(command) is str):
        info:dict = dict()
        command = command.strip()
        #? 移除空白字符
        if(command[0] == "{" and command[-1] == "}"):
            info = json.loads(command)
            #*  {
            #*      "type":"<Type of the message>",
            #*  ...
            #*  }
    elif(type(command) is dict):
        info = command
    else:
        info = None
    if(info != None):
        if("type" in info):
            for route in context.routes.keys():
                if(route == info["type"]):
                    func_name_list = context.route2funcs[route]
                    for func_full_name in func_name_list:
                        func_name = context.func_full_name2func_name[func_full_name]
                        module_name:str = context.func2module[func_full_name]
                        module = context.modules[module_name]
                        func = getattr(module, func_name)
                        await func(info, session)

# TODO 事件调用机制重做
def callEvent(event_name:str, *args, **kwargs):
    for event_n in context.events.keys():
        if(event_n == event_name):
            module_name:str = context.event2module[event_n]
            func_name:str = context.events[event_n]
            module = context.modules[module_name]
            func = getattr(module,func_name)
            tools.waitAsync(func, *args, **kwargs)

def routeRegister(route:str):
    def inner_routeRegister(func):
        func_full_name:str = tools.getModuleNameFromFunc(func) + "." + func.__name__
        if(not(func_full_name in context.registered_funcs)):
            #! 第一次加载时注册路由
            context.registered_funcs.append(func_full_name)
            context.route_func_list.append(func.__name__)
            context.routes.update({f"{route}":f"{func.__name__}"})
            context.func_full_name2func_name.update({f"{func_full_name}":f"{func.__name__}"})
            if(not route in context.route2funcs.keys()):
                context.route2funcs.update({f"{route}":[f"{func_full_name}"]})
            else:
                context.route2funcs[route].append(func_full_name)
            context.func2module.update({f"{func_full_name}":f"{tools.getModuleNameFromFunc(func)}"})
            @wraps(func)
            def wrap(*args, **kwargs):
                return func(*args, **kwargs)
            return wrap
        else:
            @wraps(func)
            def wrap(*args, **kwargs):
                return func(*args, **kwargs)
            return wrap
    return inner_routeRegister

# TODO 事件注册机制重做
def eventRegister(event:str):
    def inner_eventRegister(func):
        if(not(event in context.events.keys())):
            #! 第一次加载时注册事件
            context.event_func_list.append(func.__name__)
            context.events.update({f"{event}":f"{func.__name__}"})
            context.event2module.update({f"{event}":f"{tools.getModuleNameFromFunc(func)}"})
            @wraps(func)
            def wrap(*args, **kwargs):
                return func(*args, **kwargs)
            return wrap
        else:
            @wraps(func)
            def wrap(*args, **kwargs):
                return func(*args, **kwargs)
            return wrap
    return inner_eventRegister

def timerBasicRegister(time_sec:int = 100, type:str = "cycle", cycles:int = -1, clock = None, until = None):
    """
    基础计时器 精度较低
    计时器函数不支持参数 \n
    time_sec => 几秒执行一次 \n
    type = normal / cycle / clock \n
    clock : 哪个时间点执行 只支持一天的哪个时间点 \n
    !!! 即便使用了 clock 模式 仍然计算计时器循环 !!! \n
    until : 哪个时间点结束
    cycles => 循环执行次数 \n
    cycles -> -1 =====> 无限循环执行 \n
    cycles -> 0  =====> 不执行 \n
    normal 只执行一次 \n
    cycle 循环执行 \n
    """
    def inner_timerBasicRegister(func):
        if(not (func.__name__ in context.timers)):
            #! 第一次注册时执行
            info:dict = dict()
            info.update({
                "name" : f"{func.__name__}",
                "time_sec" : time_sec,
                "type" : type,
                "cycles" : cycles if type == "cycle" else 1,
                "clock" : clock,
                "until" : until
                })
            #! 创建新的函数供计划任务执行器调用
            @wraps(func)
            def neofunc():
                #! 后续定时器调用
                if(cycles != 0):
                    if(context.timer_info[func.__name__]["cycles"] <= -1):
                        return func()
                    #! 理论上来说 循环变量到0的时候就已经没有任何任务执行了 所以没写那行
                    elif(context.timer_info[func.__name__]["cycles"] == 1):
                        schedule.clear(func.__name__)
                        return func()
                    elif(context.timer_info[func.__name__]["cycles"] > 1):
                        context.timer_info[func.__name__]["cycles"] -= 1
                        return func()
            if(type != "clock"):
                if(cycles != 0):
                    if(until == None):
                        schedule.every(time_sec).seconds.do(neofunc).tag(func.__name__)
            else:
                if(until == None):
                    schedule.every().days.at(clock).do(neofunc)
                else:
                    schedule.every().days.at(clock).do(neofunc).until(until)
                    pass
                pass
            #* 完成注册
            context.timers.append(func.__name__)
            context.timer_info.update({
                f"{func.__name__}" : info
                })
        #* 后续普通调用
        @wraps(func)
        def wrap():
            return func()
        return wrap
    return inner_timerBasicRegister

# TODO 高级计时器 （Quartz计时器)

def initRegister(func):
    #print("after")
    @wraps(func)
    def warp():
        return func
    func()
    # do init
    #print("before")
    return warp

def load_modules():
    for module_name in config.modules:
        # module_name = ".." + module_name
        module = import_module(module_name)
        context.modules.update({f"{module.__name__}" : module})

load_modules()

