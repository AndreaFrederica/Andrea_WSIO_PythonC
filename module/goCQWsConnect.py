import asyncio
import pyjson5
import time
import websockets

from module.register import eventRegister, initRegister
from module import configIO, log
from module import register
from module import context


import config
from main import exit, term_sig_handler
from module.context import flag_exit

server_url_list = list()
tasks = list()
enable = False


# * 自定义默认配置文件字符串
cstr = (
    f"""{{
        //* ModuleName: goCQWsConnect
        enable : {configIO.p2J(enable)},
        urls : [
            "ws://127.0.0.1:8080"
        ]
}}
"""
)
# ? End

@initRegister
def init():
    global server_url_list, enable
    context.config_module_cqwsc: configIO.Config = configIO.Config(
        "cqWSClient")
    if(not context.config_module_cqwsc.defaultCheck("urls","enable")):
        context.config_module_cqwsc.setRAW_STR(cstr)
    context.config_module_cqwsc.read()
    server_url_list = context.config_module_cqwsc["urls"]
    enable = context.config_module_cqwsc["enable"]
    log.info("[CQWSC] Module CQWSC Loaded")


async def wsClient(server_url:str):
    session_name = server_url
    while not context.flag_exit:
        try:
            log.info(f"[CQWSC][{session_name}] Try to Connect the Go-CQHTTP Server -> {server_url}")
            async with websockets.connect(server_url) as websocket_client:
                context.all_cq_sessions[session_name] = websocket_client
                while True:
                    raw_message = await websocket_client.recv()
                    raw_message = raw_message.strip()
                    raw_message_dict = pyjson5.decode(raw_message)
                    #! Tag 丢弃报文
                    tag_drop_message:bool = False
                    if("retcode" in raw_message_dict.keys()):
                        raw_message_dict.update({"type":"cq_event_echo"})
                        #! 补丁 解决echo缺失类型key
                    else:
                        if("post_type" in raw_message_dict):
                            # ! 对CQ-HTTP的兼容性处理 消息路由转义
                            # * -> cq_event_<cq-type>
                            # ? post_type: message -> type: cq_event_message
                            raw_message_dict["type"] = f"cq_event_{raw_message_dict['post_type']}"
                            if(raw_message_dict["post_type"] == "meta_event"):
                                if(raw_message_dict["meta_event_type"] == "heartbeat"):
                                    #! 丢弃心跳包
                                    tag_drop_message = True
                                    pass
                        if(not tag_drop_message):
                            log.info(f"[CQWSC][{session_name}] {raw_message}")
                            await register.taskRoute(raw_message_dict, websocket_client)
        except Exception as e:
            await websocket_client.close()
            log.error(f"[CQWSC][{session_name}] {e}")
            log.error(f"[CQWSC][{session_name}] WebSocket Error")
            log.warning(f"[CQWSC][{session_name}] Wait {config.error_wait} Sec.")
            time.sleep(config.error_wait)

def getWorkList():
    global server_url, tasks, enable
    if enable:
        for server_url in server_url_list:
            tasks.append(wsClient(server_url))
        return tasks
    else:
        log.warning("[CQWSC] Please Check Setting for CQWSC")
        exit()