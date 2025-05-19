# PDFSizeAnalyzer-MCP

#### 介绍
关于PDF打印方面，统计一些页数、尺寸之类的

#### 软件架构
软件架构说明


#### 安装教程

### 1. 进入项目目录
在 Windows 系统中，可以使用以下命令进入项目目录：
```powershell
cd 替换为你的目录\pdfsize-analyzer-mcp
```

### 2. 创建虚拟环境
在 Windows 系统中，可以使用以下命令创建并激活虚拟环境：
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. 安装依赖
项目依赖 `fitz` 和 `fastmcp`，可以使用以下命令安装：
```powershell
pip install fitz fastmcp
```
或者使用国内镜像源加速安装：
```powershell
pip install fitz fastmcp -i https://pypi.tuna.tsinghua.edu.cn/simple
```


#### 使用说明

1.  确保已经按照安装教程完成环境配置。
2.  运行 `main.py` 文件：在命令行中执行 `python main.py`。
3.  按照提示输入需要分析的 PDF 文件路径。
4.  查看输出结果，程序会显示 PDF 文件的页数、尺寸等信息。

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
