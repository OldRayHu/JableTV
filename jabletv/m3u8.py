"""
 @ Author:  Ray
 @ Date  :  2022.07.22
 @ Func  :  获取并保存m3u8文件, 同时保存封面
 @ Note  :  无
"""

import re
import os
import shutil
import urllib
import requests

from bs4 import BeautifulSoup
from selenium import webdriver


def get_m3u8_file(folder,url):
    # 获取网页源代码
    option = webdriver.ChromeOptions()
    option.add_argument('--log-level=3')
    option.add_experimental_option('excludeSwitches',['enable-logging'])
    browser = webdriver.Chrome(options=option)
    browser.minimize_window()
    try:    #尝试获取m3u8地址
        browser.get(url=url)
    except: #获取失败,返回空地址,稍后重试
        browser.quit()
        return "","","",True
    htmlfile_text = browser.page_source
    browser.quit()

    # 获取m3u8文件地址
    result = re.search("https://.+m3u8", htmlfile_text)
    m3u8_url = ''
    try:
        m3u8_url = result[0]
    except: #result无结果,番号不存在
        shutil.rmtree(folder)
        return "","","",False
    m3u8urlList = m3u8_url.split('/')
    m3u8urlList.pop(-1)
    download_url = '/'.join(m3u8urlList)

    # 保存m3u8文件
    m3u8_path = os.path.join(folder, '.m3u8')
    urllib.request.urlretrieve(m3u8_url, m3u8_path)

    soup = BeautifulSoup(htmlfile_text, "html.parser")
    
    # 获取视频全名
    full_name = os.path.basename(folder)
    for meta in soup.find_all("meta"):
        if meta.get("property") == "og:title":
            full_name = meta.get("content")
            break
        else:
            continue

    # 保存影片封面
    cover_name = f"{os.path.basename(folder)}.jpg"
    cover_path = os.path.join(folder, cover_name)
    if os.path.exists(cover_path):
        return download_url, m3u8_path, full_name, True
    for meta in soup.find_all("meta"):
        meta_content = meta.get("content")
        if not meta_content:
            continue
        if "preview.jpg" not in meta_content:
            continue
        try:
            r = requests.get(meta_content)
            with open(cover_path, "wb") as cover_fh:
                r.raw.decode_content = True
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        cover_fh.write(chunk)
            print(f" NOTICE: 封面下载完成, 文件名为 {cover_name}")            
        except Exception as e:
            print(f" !ERROR: 封面下载失败, 报错为 {e}")

    return download_url, m3u8_path, full_name, True
