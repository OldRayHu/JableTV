"""
 @ Author:  Ray
 @ Date  :  2022.07.22
 @ Func  :  删除过程性文件
 @ Note  :  无
"""

import os


def delete_mp4(folder):
    files = os.listdir(folder)
    ori_mp4 = folder.split(os.path.sep)[-1] + '.mp4'
    ori_jpg = folder.split(os.path.sep)[-1] + '.jpg'
    for file in files:
        if file != ori_mp4 and file != ori_jpg:
            os.remove(os.path.join(folder, file))


def delete_m3u8(folder):
    files = os.listdir(folder)
    for file in files:
        if file.endswith('.m3u8'):
            os.remove(os.path.join(folder, file))


def delete_file(folder):
    # 删除m3u8文件
    delete_m3u8(folder)

    # 删除子mp4文件
    delete_mp4(folder)
    