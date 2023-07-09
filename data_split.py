# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：将语料进行切割，按照中文的句号进行切割，并保存到指定位置
"""

import pandas as pd
import os

def split_data_process(data):
        content = data.split('。')
        content = [x.strip().replace("\n","") for x in content if len(x.strip()) > 0]
        # 创建新的文件保存切割后的文件
        each_df = pd.DataFrame(content,columns=["text"])
        csv_save_path = os.path.join("data/data_split",data[:5]+ ".csv")
        each_df.to_csv(csv_save_path,index=False)
        return csv_save_path



if __name__ == '__main__':
    # split_data_process("data/source_data/example.csv")
    print(pd.__version__)
