from module.register import initRegister, routeRegister
from module import context
from module import log
from module.tools import json2SingleLine

@initRegister
def init():
    log.info("[andreaGroupsChat] Plugin andreaGroupsChat Loaded")

@routeRegister("event_chat")
async def groupsChat(info:dict, session: object):
    raw_message = info["message"]
    player_name = info["name"]
    namespace = info["namespace"]
    
    message = f"[{namespace}][{player_name}] {raw_message}"
    
    json_message = (f"""
        {{
            "type":"event_send_message",
            "message":"{'null' if not message else message}"
        }}""")
    for target_session in context.all_mc_sessions.values():
        if target_session != session:
            await target_session.send(json2SingleLine(json_message))