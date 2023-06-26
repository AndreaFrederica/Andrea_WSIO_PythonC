import json
import pyjson5
import requests
import wget
import os
from module import configIO, context

from module.register import initRegister
from module.configIO import path

#! Plugin Default Config
list_dir:str = "banlist"
temp_dir:str = "banlist/temp"
output_file:str = "banlist/banlist.json5"
local_list:str = "banlist/local.json5"
#? End Config

# * 自定义默认配置文件字符串
cstr = (
    f"""{{
        //? PlugName: downloadBanlist
        list_dir : "{list_dir}",
        temp_dir : "{temp_dir}",
        output_file : "{output_file}",
        local_list : "{local_list}",
        //! 在下方添加列表URL
        urls : [
                "https://gitee.com/gysdfhome/neo-uni-ban_-ban-list/raw/master/banlist.json5"
        ]
}}
"""
)

lf_cstr=(
"""
{
    // version alpha0.1
    //* 非tag段为识别字段区
    //! 内容数据格式
    //? {name:"<uid>",uuid:"<uuid>",ip:"<ip address>",muid:"<machine id>",tag:["<tagA>","<tagB>"]}
    //* ------->
    //? {
    //?     name:"<uid>",
    //?     uuid:"<uuid>",
    //?     ip:"<ip address>",
    //?     muid:"<machine id>",
    //?     tag:[
    //*         "ban",
    //*         "<tagB>"
    //?     ],
    //?     source:"<op name>",
    //?     reason:"<the reason of ban>"
    //? }
    type:"banlist",
    content:[
    ]
}
"""
)
# ? End

def downloads():
    global local_list, temp_dir, output_file, lf_cstr
    context.config_plug_downloadBanlist.read()
    json_objs:list = list()
    if(context.config_plug_downloadBanlist["urls"]):
        for url in context.config_plug_downloadBanlist["urls"]:
            try:
                file_name = wget.filename_from_url(url)
                file_all_path = f"{temp_dir}/{file_name}"
                response = requests.get(url)
                fio = open(file=file_all_path,mode="w+")
                #print("test")
                fio.write(response.content.decode(response.encoding))
                fio.close()
                #wget.download(url=url, out=file_all_path)
                fio = open(file=file_all_path,mode="r")
                json2dict = pyjson5.decode_io(fio)
                fio.close()
                json_objs.append(json2dict)
            except:
                print(f"DOWNLOAD ERROR  {url}")
    try:
        fio = open(file=local_list,mode="r")
        json2dict = pyjson5.decode_io(fio)
        fio.close()
        json_objs.append(json2dict)
    except:
        fio = open(file=local_list,mode="w+")
        fio.write(lf_cstr)
        fio.close()
        print(f"ERROR IN LOCAL LIST")
    summary_dict:dict = {
        "type":"banlist",
        "content":[]
    }
    if(json_objs):
        for data_obj in json_objs:
            for item in data_obj["content"]:
                summary_dict["content"].append(item)
    fio = open(file=output_file,mode="w+")
    fio.write(json.dumps(summary_dict, sort_keys=True, indent=4, separators=(',', ':')))
    fio.close()


@initRegister
def init():
    global temp_dir, output_file, local_list, cstr, list_dir
    # * 写入默认自定义配置文件
    context.config_plug_downloadBanlist: configIO.Config = configIO.Config("downloadBanlist")
    if (not context.config_plug_downloadBanlist.defaultCheck("temp_dir", "output_file", "urls", "local_list", "list_dir")):
        context.config_plug_downloadBanlist.setRAW_STR(cstr)
    context.config_plug_downloadBanlist.read()
    temp_dir = context.config_plug_downloadBanlist["temp_dir"]
    output_file = context.config_plug_downloadBanlist["output_file"]
    local_list = context.config_plug_downloadBanlist["local_list"]
    list_dir = context.config_plug_downloadBanlist["list_dir"]
    path = list_dir
    if(not os.path.exists(path)):
        os.mkdir(path)
    path = temp_dir
    if(not os.path.exists(path)):
        os.mkdir(path)
    downloads()






def test():
    url = 'https://p0.ifengimg.com/2019_30/1106F5849B0A2A2A03AAD4B14374596C76B2BDAB_w1000_h626.jpg'

    # 获取文件名
    file_name = wget.filename_from_url(url)
    print(file_name)  #1106F5849B0A2A2A03AAD4B14374596C76B2BDAB_w1000_h626.jpg

    # 下载文件，使用默认文件名,结果返回文件名
    file_name = wget.download(url)
    print(file_name) #1106F5849B0A2A2A03AAD4B14374596C76B2BDAB_w1000_h626.jpg

    # 下载文件，重新命名输出文件名
    target_name = 't1.jpg'
    file_name = wget.download(url, out=target_name)
    print(file_name) #t1.jpg