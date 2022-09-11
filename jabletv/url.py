"""
 @ Author:  Ray
 @ Date  :  2022.07.22
 @ Func  :  获取待下载影片的url列表
 @ Note  :  无
"""

import re
import random
import argparse

from bs4 import BeautifulSoup
from selenium import webdriver
from jabletv.config import jable_url, base_url


def init_parser():
    parser = argparse.ArgumentParser(description="JableTV Downloader")
    parser.add_argument('-r','--rand', type=bool, default=False,
        help="Enter True for random download")
    parser.add_argument('-f','--file', type=bool, default=False,
        help="Enter True to download according to file's contant")
    parser.add_argument('-u','--url', type=str, default="",
        help="Jable TV URLs to download, divided by \',\'")
    parser.add_argument('-n','--name', type=str, default="",
        help="Jable TV names to download, divided by \',\'")
    return parser


def random_download():
    browser = webdriver.Chrome()
    browser.minimize_window()
    browser.get(url=jable_url)
    web_content = browser.page_source
    browser.quit()
    soup = BeautifulSoup(web_content, 'html.parser')
    h6_tags = soup.find_all('h6', class_='title')
    av_list = re.findall(r'https[^"]+', str(h6_tags))
    return random.choice(av_list)


def get_url():
    parser = init_parser()
    args = parser.parse_args()
    
    url_list = []
    input_str = ""
    if (len(args.url)==0) and (len(args.name)==0) and (args.rand is False) and (args.file is False):
        input_str = input('-输入单个jable网址:')
        url_list.append(input_str)
    elif (len(args.url)!=0):
        input_str = args.url
        url_list = input_str.split(',')
    elif (len(args.name)!=0):
        input_str = args.name
        input_list = input_str.split(',')
        for i in input_list:
            url_list.append(base_url+i.lower()+'/')
    elif (args.rand is True):
        input_str  = random_download()
        url_list.append(input_str)
    elif (args.file is True):
        file = open('download.txt','r')
        for line in file:
            line = line.replace("\n","")
            url_list.append(base_url+line.lower()+'/')
    
    return url_list