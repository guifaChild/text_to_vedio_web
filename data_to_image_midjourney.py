# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月08日
描述：
"""
import asyncio
import os.path
import pandas as pd
from midjourney.app .handler import prompt_handler
from midjourney.util._queue import taskqueue
from midjourney.lib.api import discord
import fileinput
import json
import requests
import json

# 构造请求的 URL 和 JSON 参数


def SaveImgFromUrl(response, save_path):
    numOfOutput = len(response)
    org_path = save_path
    for i in range(numOfOutput):
        save_path = org_path
        img_content = requests.get(response[i]["url"]).content
        if i >= 1:
            save_path = save_path.split(".")[0] + "_" + str(i + 1) + "." + save_path.split(".")[1]
        with open(save_path, "wb") as f:
            f.write(img_content)



async def my_async_function(trigger_id,prompt):
    loop = asyncio.get_running_loop()
    # 在这里执行异步操作
    taskqueue.put(trigger_id, discord.generate, prompt)


def CreateImage(description):
    url = "http://127.0.0.1:8062/v1/api/trigger/imagine"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": description
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 获取响应内容
    response_data = response.json()
    return "**<#"+response_data['trigger_id']+"#>"


def image_url(data_id_content,line):
    if "fetch - Fetch: xxx, " in line and data_id_content in line and ".png" in line:
        data_line = line.split("fetch - Fetch: xxx, ")[1]
        result = data_line.split(", 'proxy_url': '")[1].split("', 'size':")[0]
        print(result)
        return result
    else:
        return ""


import requests
from PIL import Image

def save_image_from_url(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print("图像已保存：", save_path)


def load_image_data_midjourney(path):
    print("最新的内容显示")
    lists=[]
    df = pd.read_csv(path)
    newpath = path.split(".csv")[0].replace("data_prompt", "data_image")
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for index, row in df.iterrows():
        data_id_content = CreateImage(row["prompt"])
        # 监听文件的内容变化
        with open("midjourney/log/mj-api.log","r") as log_file :
            label ="meiyou"
            while True :
                if label == "hanyou" :
                    break
                lines = log_file.readlines()
                for line in lines:
                    image_urls = image_url(data_id_content,line.strip())
                    if image_urls != "" and image_urls not in lists:
                        lists.append(image_urls)
                        label="hanyou"
                        break

    for index, row in df.iterrows():
        childpath = os.path.join(newpath,str(index)+".png")
        save_image_from_url(lists[index],childpath)
    return newpath

if __name__ == '__main__':
    lists=[]
    with open("midjourney/log/mj-api.log", "r") as log_file:
        label = "meiyou"
        while True:
            if label == "hanyou":
                break
            lines = log_file.readlines()
            for line in lines:
                image_urls = image_url("<#6165796329#>", line.strip())
                if image_urls != "" and image_urls not in lists:
                    lists.append(image_urls)
                    label = "hanyou"
                    break
