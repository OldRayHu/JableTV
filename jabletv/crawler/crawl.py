"""
 @ Author:  Ray
 @ Date  :  2022.07.22
 @ Func  :  爬取子文件 
 @ Note  :  无
"""

import os
import time
import copy
import requests
import concurrent.futures

from functools import partial
from jabletv.config import headers


def scrape(ci, folderPath, downloadList, urls):
    os.path.split(urls)
    fileName = urls.split('/')[-1][0:-3]
    saveName = os.path.join(folderPath, fileName + ".mp4")
    if os.path.exists(saveName):
        # 跳过已下载
        print('\r  -PROCESS: 当前目标 {0} 已下载, 剩余 {1} 个'.format(
            urls.split('/')[-1], len(downloadList)), end='', flush=True)
        downloadList.remove(urls)
    else:
        response = requests.get(urls, headers=headers, timeout=10)
        if response.status_code == 200:
            content_ts = response.content
            if ci:
                content_ts = ci.decrypt(content_ts)  # 解碼
            with open(saveName, 'ab') as f:
                f.write(content_ts)
            downloadList.remove(urls)
        # 输出进度
        print('\r  -PROCESS: 正在下载 {0}, 剩余 {1} 个, status code: {2}'.format(
            urls.split('/')[-1], len(downloadList), response.status_code), end='', flush=True)


def startCrawl(ci, folderPath, downloadList):
    round = 0
    while(downloadList != []):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(partial(scrape, ci, folderPath,
                                 downloadList), downloadList)
        round += 1
        print(f', round {round}')


def crawl(ci, folder, ts_list):
    download_list = copy.deepcopy(ts_list)
    start_time = time.time()
    print(' NOTICE: 开始下载 ' + str(len(download_list)) + ' 份文件, ', end='')
    print('预计等待时间 {0:.2f} 分钟(视影片长度和网络速度而定)'.format(len(download_list) / 150))

    startCrawl(ci, folder, download_list)   #开始爬取

    end_time = time.time()
    print(' NOTICE: 下载成功, 共计 {0:.2f} 分钟'.format((end_time - start_time) / 60))
