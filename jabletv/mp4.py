"""
 @ Author:  Ray
 @ Date  :  2022.07.22
 @ Func  :  爬取mp4片段后合并mp4
 @ Note  :  无
"""

from jabletv.crawler.crawl  import  crawl
from jabletv.crawler.merge  import  merge_mp4


def get_mp4_file(ci, ts_list, folder):
    # 爬取mp4片段至文件夹
    crawl(ci, folder, ts_list)

    # 合成mp4文件
    merge_mp4(folder, ts_list)
