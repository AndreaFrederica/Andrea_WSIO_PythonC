import asyncio
import inspect
import pyjson5
import re


def getModuleNameFromFunc(func):
    temp:str = inspect.getmodule(func)
    """
    output:str = ""
    tag:int = 0
    for i in temp:
        if(i == "\'"):
            tag += 1
        if(tag == 1):
            output += i
    """
    return temp.__name__

def getClassNameFromFunc(func):
    temp = ""
    for i in func.__qualname__:
        if(i == "."):
            break
        temp += i
    return temp

def waitAsync(func, *args, **kwargs):
    if(inspect.iscoroutinefunction):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()
    else:
        func(*args, **kwargs)

def json2SingleLine(json_str: str):
    return pyjson5.encode(pyjson5.decode(json_str))

#! 此方法被弃用！
def getObjName(p:object) -> str:
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)