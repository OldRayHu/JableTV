"""
 @ Author:  Ray
 @ Date  :  2022.09.11
 @ Func  :  工程执行文件
 @ Note  :  无
 @ Args  :  -h --help 获取帮助
            -r --rand 随机影片, True/Flase
            -f --file 根据文件下载, True/Flase
            -i --info 保存其他信息, True/False
            -u --url  地址列表, 使用','分割
            -n --name 番号列表, 使用','分割, 不区分大小写
"""

import os

from jabletv.url    import  get_url
from jabletv.folder import  get_folder
from jabletv.m3u8   import  get_m3u8_file
from jabletv.ts     import  get_ts_list
from jabletv.delete import  delete_file
from jabletv.mp4    import  get_mp4_file


def app():
    done_list = []      #已完成列表
    failed_list = []    #未完成列表

    ## 获取待下载影片的url列表
    url_list, save_info = get_url()

    ## 循环下载影片
    while(url_list != []):
        url = url_list[-1]

        # 1.过滤影片 + 建立文件夹
        is_done, folder_path = get_folder(url)

        name = folder_path.split('\\')[-1]
        if not is_done:
            print("\n--------------------------------------------------------------------")
            print(f"-影片 {name} 开始下载, 剩余 {len(url_list)-1} 个待下载")

            # 2.获取并保存m3u8文件 + 保存封面
            download_url, m3u8_path, full_name, exist = get_m3u8_file(folder_path, url)
            if not exist:                   #番号不存在
                url_list.pop()
                print(f" !ERROR: {name} 不存在或网站无资源")
                failed_list.append(name)
            elif len(download_url) == 0:    #链接失败
                print(f" !ERROR: {url} 连接失败, 稍后重试")
            else:
                # 3.根据m3u8文件获取ts列表
                ci, ts_list = get_ts_list(download_url, m3u8_path)

                # 4.爬取mp4片段 + 合并mp4
                get_mp4_file(ci, ts_list, folder_path)

                # 5.刪除过程性文件
                delete_file(folder_path)

                # 6.(可选)修改文件夹名
                if save_info is True:
                    old_dir_name = folder_path
                    os.chdir("video")
                    new_dir_name = os.path.join(os.getcwd(), full_name)
                    os.chdir("../")
                    os.rename(old_dir_name, new_dir_name)

                done_list.append(name)
                print(f"-影片 {name} 下载完成")
                url_list.pop()
        else:
            done_list.append(name)
            url_list.pop()
    
    ## 输出结束提示
    print("\n--------------------------------------------------------------------")
    print(f"-本次成功下载 {len(done_list)} 个影片, 共有 {len(failed_list)} 个不存在的番号")
    print("  -成功: ", end='')
    for i in done_list:
        print(i, end=' ')
    print("\n  -失败: ", end='')
    for i in failed_list:
        print(i, end=' ')
    print("")


if __name__ == '__main__':
    app()
