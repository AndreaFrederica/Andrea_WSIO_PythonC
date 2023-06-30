#! 需要使用事件注册器的模块在此声明
from module.log import error

modules:list = [
    #! 模块和插件无本质区别 只是模块本身更嵌入框架罢了
    #! 此处排序影响加载顺序
    #* 模块
    "module.configIO",
    #* 插件
    "plugin.downloadBanlist",
    "plugin.kickCheck",
    #"plugin.test"
]
#! 配置文件编码
encode:str = "utf-8"
#! 主线程错误等待时间
error_wait:int = 10
