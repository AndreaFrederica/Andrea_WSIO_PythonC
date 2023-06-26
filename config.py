#! 需要使用事件注册器的模块在此声明
modules:list = [
    #! 模块和插件无本质区别 只是模块本身更嵌入框架罢了
    #! 此处排序影响加载顺序
    #* 模块
    "module.configIO",
    #* 插件
    "plugin.downloadBanlist",
    "plugin.kickCheck",
    "plugin.test"
]
encode:str = "utf-8"
