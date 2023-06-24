import asyncio
from functools import wraps
import functools
from importlib import import_module
import json
from typing import Any
from module import context
from module import tools
import config



async def taskRoute(command:str):
    if(command[0] == "{" and command[-1] == "}"):
        info = json.loads(command)
        #*  {
        #*      "type":"<Type of the message>",
        #*  ...
        #*  }
        for route in context.routes.keys():
            if(route == info["type"]):
                module_name:str = context.route2module[route]
                func_name:str = context.routes[route]
                module = context.modules[module_name]
                func = getattr(module, func_name)
                await func(info)

def routeRegister(route:str):
    def inner_routeRegister(func):
        if(not(route in context.routes.keys())):
            #! 第一次加载时注册路由
            context.route_func_list.append(func.__name__)
            context.routes.update({f"{route}":f"{func.__name__}"})
            context.route2module.update({f"{route}":f"{tools.getModuleNameFromFunc(func)}"})
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
        context.modules.update({f"{module.__name__}":module})

load_modules()

