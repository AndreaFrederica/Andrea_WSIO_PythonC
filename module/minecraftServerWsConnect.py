import asyncio
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
        //* ModuleName: minecraftServerWsConnect
        enable : {configIO.p2J(enable)},
        urls : [
            "ws://localhost:23080"
        ]
}}
"""
)
# ? End

@initRegister
def init():
    global server_url_list, enable
    context.config_module_mcwsc: configIO.Config = configIO.Config(
        "mcWSClient")
    if(not context.config_module_mcwsc.defaultCheck("urls","enable")):
        context.config_module_mcwsc.setRAW_STR(cstr)
    context.config_module_mcwsc.read()
    server_url_list = context.config_module_mcwsc["urls"]
    enable = context.config_module_mcwsc["enable"]
    log.info("[MCWSC] Module MCWSC Loaded")


async def wsClient(server_url:str):
    session_name = server_url
    while not context.flag_exit:
        try:
            log.info(f"[MCWSC][{session_name}] Try to Connect the MinecraftServer -> {server_url}")
            async with websockets.connect(server_url) as websocket_client:
                context.all_mc_sessions[session_name] = websocket_client
                while True:
                    message = await websocket_client.recv()
                    log.info(f"[MCWSC][{session_name}] {message}")
                    await register.taskRoute(message, websocket_client)
        except Exception as e:
            await websocket_client.close()
            log.error(f"[MCWSC][{session_name}] {e}")
            log.error(f"[MCWSC][{session_name}] WebSocket Error")
            log.warning(f"[MCWSC][{session_name}] Wait {config.error_wait} Sec.")
            time.sleep(config.error_wait)

def getWorkList():
    global server_url, tasks, enable
    if enable:
        for server_url in server_url_list:
            tasks.append(wsClient(server_url))
        return tasks
    else:
        log.warning("[MCWSC] Please Check Setting for MCWSC")
        exit()