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
pip install pymupdf fastmcp -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 生成配置文件（以Trae为例）
运行 `generate_config.py` 文件生成 `mcp_config.json`：
在命令行中执行
```powershell
python generate_config.py
```

将自动生成 `mcp_config.json` 文件，内容如下：
```json
{
    "mcpServers": {
        "PDFAnalyzer": {
            "command": "虚拟环境中的python.exe",
            "args": [
                "主程序main.py的完整路径"
            ]
        }
    }
}
```
#### 使用说明

1.  确保已经按照安装教程完成环境配置。
2.  在'Trae'软件中，新增MCP，填入配置json内容。
3.  测试运行，确保配置正确。
- 测试1：调用mcp服务，告诉我一下这个pdf文件的页数吗？
- 测试2：调用mcp服务，按打印尺寸分别统计下页数和页码？


#### 注意事项

-   确保使用的是虚拟环境中的 Python 解释器，涉及到依赖问题。
-   先用纯英文目录测试，成功后再测试中文目录。
