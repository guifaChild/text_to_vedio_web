# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年07月08日
描述：将生成的语音、图像合成视频
"""

import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import numpy as np

def flFunc(gf, t):  # 变换主函数
    return frameScroll(gf(t), 2)  # 一帧往前滚动2行


def frameScroll(frame, x):  # 实现帧数据环绕滚动x行
    global framePos, clipHeight

    moveCount = framePos + x  # 本次移动行数在前一次行数基础上加x行
    if moveCount > clipHeight:  # 环绕判断处理，其实用moveCount %= clipHeight语句更简洁效果相同，但取余的运算效率低一些
        moveCount -= clipHeight
    framePos = moveCount  # 记录本次移动的行数
    remainFrame = frame[:moveCount]  # 取前moveCount-1行
    exceedFrame = frame[moveCount:]  # 取后面剩余行

    return np.vstack((exceedFrame, remainFrame))  # 将两部分数据叠加实现环绕效果，返回作为变换后的帧



def merge_vedio_mid(image_dir_path,audio_dir_path):


    # 将文件名按照顺序排列
    image_files = sorted(os.listdir(image_dir_path))
    audio_files = sorted(os.listdir(audio_dir_path))

    clips = []

    # 图片和音频的持续时间
    duration = 4  # 您可以根据需要调整此值
    speed =10
    size =700


    for i in range(0, len(image_files), 4):
        image_paths = [os.path.join(image_dir_path, image_files[i + j]) for j in range(4)]
        audio_path = os.path.join(audio_dir_path, audio_files[i // 4])

        print(image_paths)
        durations = [1] * 4
        image_clip = ImageSequenceClip(image_paths, durations=durations)


        audio_clip = AudioFileClip(audio_path)

        fl = lambda gf, t: gf(t)[int(speed * t):int(speed * t) + size,:]

        image_clip = image_clip.set_position(('center', 'center')).fl(fl,apply_to=['mask']).set_duration(audio_clip.duration)

        clip = image_clip.set_audio(audio_clip)


        clips.append(clip)

    # 将所有剪辑合并成一个视频
    final_clip = concatenate_videoclips(clips)
    new_parent = image_dir_path.replace("data_image","data_vedio").split("story")[0]
    # 导出视频
    if not os.path.exists(new_parent):
        os.makedirs(new_parent)
    new_path = image_dir_path.replace("image_split","data_vedio_midjourney")
    final_clip.write_videofile(new_path+".mp4", fps=24,audio_codec="aac")  # 可以根据需要调整fps值
    return new_path+".mp4"

if __name__ == '__main__':
    merge_vedio_mid("data/image_split/只听到几声","data/data_audio/只听到几声")


