## How to run
### Environment Install
1. ChromeDriver 下载&解压&复制到chrome目录&环境变量配置

### Run
1. 关闭所有chrome的后台进程

2. 本地创建一个空的文件夹用于保存chrome数据

3. win + R 键打开运行窗口，输入cmd然后回车 

4. 在命令行中输入 chrome.exe --remote-debugging-port=9222 --user-data-dir="这里填你刚才创建的空文件夹的绝对路径" 然后回车，这时会自动打开一个新的chrome浏览器，不要关闭它

4. 运行程序, 会有界面逐步提示操作步骤

5. 如果程序运行中出现问题，则可以关闭Chrome当前页面(不用关闭浏览器)，然后重新运行
