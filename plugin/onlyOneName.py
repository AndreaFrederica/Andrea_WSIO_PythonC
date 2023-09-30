from module import tools, log
from module.register import initRegister, routeRegister
from module.tools import json2SingleLine


@initRegister
def init():
    log.info("[onlyOneName] Plugin onlyOneName Loaded")

@routeRegister("event_login")
async def oneName(info: dict, session: object):
    flag_error:bool = False
    reason:str = ""
    uuid:str = info["uuid"]
    name:str = info["name"]
    online_players:list = info["players"]
    for player in online_players:
        if(name == player["name"]):
            reason = "ID重复"
            flag_error = True
            break
        if(uuid == player["uuid"]):
            reason = "UUID重复"
            flag_error = True
            break
    if(flag_error):
        message:str =tools.json2SingleLine (f"""
            {{
                "type":"event_advance_check_return",
                "result":false,
                "uuid":"{info['uuid']}",
                "message":"{reason}"
            }}
            """)
    else:
        message:str =tools.json2SingleLine (f"""
            {{
                "type":"event_advance_check_return",
                "result":true,
                "uuid":"{info['uuid']}",
                "message":"PASS"
            }}
            """)
        
    await session.send(message)