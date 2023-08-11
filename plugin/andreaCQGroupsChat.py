from module.register import initRegister, routeRegister
from module import configIO, context
from module import log
from module.tools import json2SingleLine

group_id:int = 111111111
cq_namespace:str = "测试群消息"

@initRegister
def init():
    global cq_namespace, group_id
    context.config_plug_cqGroupChat:configIO.Config = configIO.Config("cqGroupChat")
    config_obj:configIO.Config = context.config_plug_cqGroupChat
    group_id =  config_obj.setDefault("group_id", group_id)
    cq_namespace = config_obj.setDefault("namespace", cq_namespace)
    config_obj.commit()
    log.info("[andreaCQGroupsChat] Plugin andreaCQGroupsChat Loaded")

#! 监听CQ-HTTP消息
@routeRegister("cq_event_message")
async def cqGroupsChat(info:dict, session: object):
    global group_id, cq_namespace
    if(info["message_type"] == "group"):
        if(info["group_id"] == group_id):
            raw_message = info["message"]
            sender_name = info["sender"]["nickname"]
            
            message = f"[{cq_namespace}][{sender_name}] {raw_message}"
            
            json_message = (f"""
                {{
                    "type":"event_send_message",
                    "message":"{'null' if not message else message}"
                }}""")
            for target_session in context.all_mc_sessions.values():
                await target_session.send(json2SingleLine(json_message))


#! 监听MC服务端消息
@routeRegister("event_chat")
async def groupsChat(info:dict, session: object):
    global group_id
    raw_message = info["message"]
    player_name = info["name"]
    namespace = info["namespace"]
    
    message = f"[{namespace}][{player_name}] {raw_message}"
    
    json_message = (f"""
        {{
            "action":"send_group_msg",
            "params":{{
                "group_id":{group_id},
                "message":"{message}",
                "auto_escape":false
            }}
        }}""")
    for target_session in context.all_cq_sessions.values():
        await target_session.send(json2SingleLine(json_message))