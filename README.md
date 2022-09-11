# JableTV

> JableTV Web Video Downloader
>
> **P.S. 更多材料，请联系邮箱 rayhuc@163.com，并备注说明来意**

<br/>

### (一) 基本信息

- 作者：Ray
- 时间：2022-09-11
- 备注：
  - 项目受到 [原工程](https://github.com/hcjohn463/JableTVDownload) 的启发；
  - 个人无聊时编写的代码，无其他意图；
  - 代码中没有添加代理 VPN，使用者需要自行连接 VPN；

<br/>


### (二) 环境配置

#### 1. 安装虚拟环境和必要包

- 可以选择使用 pipenv 一键安装虚拟环境和包

  ```bash
  pipenv install
  pipenv shell
  ```

- 或选择使用 virtual env 和 requirements.txt 安装

  ```bash
  python3 -m venv jable
  pip install -r requirements.txt
  ```
  



#### 2. 下载 Webdriver

- 按照电脑安装 Chrome 的版本，在 [ChromeDriver 网站](https://chromedriver.chromium.org/) 下载对应的 Webdriver；
- 将下载好的文件放在 `..\python\Scripts` 文件夹下；
- 使用 Pycharm 的再复制到 `..\site-packages\selenium\webdriver\chrome` 下；



#### \*3. 安装 ffmpeg

- 安裝 [FFmpeg](https://ffmpeg.org/) (不安装也能下载，但影片拖拉时间轴会有卡帧情况)

<br/>

### (三) 项目运行

#### 1. 启动虚拟环境 (shell)
- 双击打开 `env.bat` 批处理文件，进入命令行；



#### 2. 下载影片 (execute)

- 根据 url 单独下载：执行以下指令，并根据提示输入要下载影片的 url 网址；

  ```bash
  python main.py
  ```

- 根据 url 批量下载：执行以下指令，url 网址用 `,` 隔开；

  ```bash
  python main.py -u url1,url2,url3,...
  ```

- 根据番号批量下载：执行以下指令，番号用 `,` 隔开；

  ```bash
  python main.py -n cawd-274,cawd-386,ipx-468,...
  ```

- 随机推荐影片下载：执行以下指令

  ```bash
  python main.py -r True
  ```

- 将番号提前写入 `download.txt` 文件，根据文件下载：执行以下指令

  ```bash
  python main.py -f True
  ```

**P.S. 要执行的指令可以提前写入 `do.bat` 文件中，运行时在命令行输入 `do.bat` 即可；** 

​		**(不修改 `do.bat` 时，默认根据 `download.txt` 下载)**



#### 3. 等待下载 (wait)  

- 项目先下载封面，再下载影片；
- 中间会弹出最小化的谷歌浏览器，不要点击，会自动关闭；
- 下载时会有进度提示；
- 下载好的影片会保存在 video 文件夹下的对应番号子文件夹中；



#### 4. 后续处理 (process)

- 使用 ffmpeg 可以对影片的格式进行更多的处理；
