# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月7日
描述：项目启动项

"""
from flask import Flask, render_template,request
import webbrowser
import threading
import pandas as pd

from data_promt_words import load_data_text
from data_split import split_data_process
from data_to_image import load_image_data
from data_to_image_midjourney import load_image_data_midjourney
from data_to_vedio import merge_vedio
from data_to_vedio_midjourney import merge_vedio_mid
from data_tts import load_source_data_text
from midjourney.task_bot import start_robot
from image_split import  image_split_data

app = Flask(__name__)

@app.route('/')
def index():
    data = pd.read_csv("data.csv")
    table = data.to_html(index=False, table_id="my-table")
    return render_template('index.html',table=table)

@app.route('/save', methods=['POST'])
def save_data():
    table_data = request.json  # 获取传递的表格数据

    # 将表格数据保存到 Pandas DataFrame
    df = pd.DataFrame(table_data, columns=['Column1', 'Column2'])  # 替换为实际的列名
    df.to_csv('data.csv', index=False,header=False)  # 将 DataFrame 保存为 CSV 文件

    return '数据保存成功！'


@app.route('/send', methods=['POST'])
def receive_text():
    pdata = pd.read_csv("data.csv")
    api_key = pdata.iloc[5, 1]
    data = request.get_json()
    text = data.get('text')
    text = text.replace(" ","").replace(" ","")
    data_path = split_data_process(text)
    data_prompt_path = load_data_text(data_path,api_key)
    tts_key = pdata.iloc[1, 1]
    tts_url = pdata.iloc[3, 1]
    tts_region = pdata.iloc[2, 1]
    tts_data = load_source_data_text(data_path,tts_key,tts_url,tts_region)
    if len(pdata.iloc[7, 1]) < 10:
        iamge_source= load_image_data(data_prompt_path,api_key)
        path_vedio = merge_vedio(iamge_source, tts_data)
    else :
        print("走midjourney")
        iamge_source = load_image_data_midjourney(data_prompt_path)
        image_split = image_split_data(iamge_source)
        path_vedio= merge_vedio_mid(image_split, tts_data)


    return path_vedio


def load_data():
    data = pd.read_csv("data.csv")
    return data

def open_browser():
    # 在启动后延迟几秒钟打开浏览器，确保Flask应用已经开始运行
    print("打开浏览器")
    webbrowser.open('http://localhost:5000')




if __name__ == '__main__':
    # 创建一个新线程来打开浏览器
    thread = threading.Timer(1,open_browser)
    thread.start()
    app.run()
    # load_data()