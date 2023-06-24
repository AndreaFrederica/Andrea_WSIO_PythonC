import time
from module import configIO, context
import config
from module.router import routeRegister, initRegister
import pyjson5

#! 范例插件
#! 注册一个插件需要在 config.py 的 modules 中 进行注册
#* 例如 "task_route.kickCheck"

#* 自定义默认配置文件字符串
cstr = (
f"""{{
        //* PlugName: kickCheck
        enable_ip:false,                 //! 启用ip识别
        enable_name:true,                //* 启用名字识别
        enable_uuid:true,                //* 启用UUID识别
        //? FullSearch
        enable_full_search:false         //! 启用全索检  切勿启用 可能会导致bug
}}
"""
)
#? End
#! Plug Default Config
enable_ip:bool = False
enable_name:bool = True
enable_uuid:bool = True
#? FullSearch
enable_full_search:bool = False                         #! 功能还没做好 开了会炸！
#* End Config

def loadBanList():
        fp = open("test.json5", mode="r", encoding=config.encode)
        context.ban_list = pyjson5.decode_io(fp=fp)
        fp.close()

#* 使用 @initRegister 注册插件的初始化函数
@initRegister
def init():
        global enable_ip, enable_name, enable_uuid, enable_full_search
        loadBanList()
        #* 基础版配置文件生成器
        # context.config_plug_kickCheck:configIO.Config = configIO.Config("kickCheck")
        # enable_ip =  context.config_plug_kickCheck.setDefault("enable_ip", enable_ip)
        # enable_name = context.config_plug_kickCheck.setDefault("enable_name", enable_name)
        # enable_uuid = context.config_plug_kickCheck.setDefault("enable_uuid", enable_uuid)
        # enable_full_search = context.config_plug_kickCheck.setDefault("enable_full_search", enable_full_search)
        # context.config_plug_kickCheck.commit()
        #? End
        #* 写入默认自定义配置文件
        context.config_plug_kickCheck:configIO.Config = configIO.Config("kickCheck")
        if(not context.config_plug_kickCheck.defaultCheck("enable_ip", "enable_name", "enable_uuid", "enable_full_search")):
                context.config_plug_kickCheck.setRAW_STR(cstr)
        #? End

#* 使用 @routeRegister("<route>") 注册路由函数
@routeRegister("event_login")
async def kickCheck(info:dict):
        global enable_ip, enable_name, enable_uuid, enable_full_search
        flag_fined:bool = False
        for i in context.ban_list["content"]:
                find = "name"
                if(i[find] == info[find] and enable_name):
                        flag_fined = True
                        if(enable_full_search):
                                pass
                        else:
                                break
                find = "uuid"
                if(i[find] == info[find] and enable_uuid):
                        flag_fined = True
                        if(enable_full_search):
                                pass
                        else:
                                break
                find = "ip"
                if(i[find] == info[find] and enable_ip):
                        flag_fined = True
                        if(enable_full_search):
                                pass
                        else:
                                break
        time.sleep(0.5)
        if(flag_fined and ("ban" in i["tag"])):
                await context.context.send(f"kick uuid {info['uuid']} test")

@routeRegister("event_reload_ban_list")
async def reloadBanList(info:dict):
        loadBanList()