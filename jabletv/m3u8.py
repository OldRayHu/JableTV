"""
 @ Author:  Ray
 @ Date  :  2023.01.31
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
    
    # 获取视频新名字
    # (1)获取原名称
    is_found_1 = False
    full_name = ''
    for meta in soup.find_all("meta",{"property":"og:title"}):
        full_name = meta.get("content")
        is_found_1 = True
    if not is_found_1:
        raise KeyError
    # (2)寻找影片女优名
    actress_name_list = []
    for span in soup.find_all("span",{'class':'placeholder rounded-circle'}):
        a_name = span.get("data-original-title")
        actress_name_list.append(a_name)
    for img in soup.find_all("img",{'class':'avatar rounded-circle'}):
        a_name = img.get("data-original-title")
        actress_name_list.append(a_name)
    # (3)组织新名字
    full_name_spt = full_name.split(' ')
    #  (a)part-1 番号
    part1 = folder.lower()
    #  (b)part-2,3 演员和影片名字
    actress_num = len(actress_name_list)
    if actress_num == 0:    # 没有演员
        part2 = '[]'
        part3 = ' '.join(full_name_spt[1:])
    elif actress_num >= 5:  # 大于等于5个演员
        part2 = '[G'+str(actress_num)+']'
        part3 = ' '.join(full_name_spt[1:])
    elif len(full_name_spt)-2 < actress_num:  # 名字里演员数不足
        part2 = ''.join(['['+i+']' for i in actress_name_list])
        part3 = ' '.join(full_name_spt[1:])
    else:   # 演员数量足够
        part2 = ''.join(['['+i+']' for i in full_name_spt[-actress_num:]])
        part3 = ''.join([' '+i for i in full_name_spt[1:-actress_num]])
    #  (c)拼接完整名字
    new_name = part1+'-'+part2+'-'+part3[1:]

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

    return download_url, m3u8_path, new_name, True
