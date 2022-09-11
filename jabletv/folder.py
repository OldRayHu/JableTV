"""
 @ Author:  Ray
 @ Date  :  2022.07.21
 @ Func  :  判断影片是否已经下载, 建立文件夹
 @ Note  :  无
"""

import os


def get_folder(url):
    is_done = False
    url_split = url.split('/')
    dirName = url_split[-2]

    os.chdir("video")
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    elif os.path.exists(dirName+'\\'+dirName+'.mp4'):
        is_done = True
    folder_path = os.path.join(os.getcwd(), dirName)
    os.chdir("../")
    
    return is_done, folder_path
