# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月08日
描述：
"""
import os

from PIL import Image


def split_image_quadrants(image_path, output_dir):
    # 打开原始图像
    image = Image.open(image_path)
    width, height = image.size

    # 计算切割后每个象限的大小
    quadrant_width = width // 2
    quadrant_height = height // 2

    # 切割图像并保存四个象限
    for i in range(2):
        for j in range(2):
            left = i * quadrant_width
            top = j * quadrant_height
            right = left + quadrant_width
            bottom = top + quadrant_height

            quadrant = image.crop((left, top, right, bottom))
            file_name = image_path.split("/")[-1].split(".png")[0]
            # 构建输出文件路径
            output_path = f"{output_dir}/{file_name}_{i}{j}.png"

            # 保存切割后的象限
            quadrant.save(output_path)


def image_split_data(image_path):
    files_path =[os.path.join(image_path,file) for file in os.listdir(image_path)]
    out_putdir = image_path.replace("data_image","image_split")
    if  not os.path.exists(out_putdir):
        os.makedirs(out_putdir)
    for item in files_path :
        split_image_quadrants(item,out_putdir)
    return out_putdir


if __name__ == '__main__':

    # 示例：按四象限结构切割图像并保存
    image_split_data("data/data_image/只听到几声/")