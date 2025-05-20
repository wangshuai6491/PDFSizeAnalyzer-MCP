# PDFSizeAnalyzer-MCP

## mcp工具介绍
### 1.统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计 A3、A4等常见尺寸纸张的数量和页码范围

def analyze_pdf_pages(file_path: str) -> tuple:
    """
    统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计 A3、A4等常见尺寸纸张的数量和页码范围。
    参数:
        file_path (str): 单个PDF 文件的路径。
    返回:
        tuple: 包含两个元素的元组，第一个元素是 PDF 的总页数 (int)，第二个元素是一个列表 (list)，
               列表中的每个元素是一个字典，包含纸张尺寸、纸张类型、总页数和页码范围。
    """
### 2.将 PDF 的每一页转换为图片，并保存到以 PDF 名称命名的文件夹中。
def convert_pdf_to_images(file_path: str)-> list:
    """
    将 PDF 的每一页转换为图片，并保存到以 PDF 名称命名的文件夹中。
    参数:
        file_path (str): 单个 PDF 文件的路径。
    返回:
        list: 包含所有生成图片文件路径的列表。
    """

### 3.按章节或1级书签拆分PDF文件，返回包含章节信息和保存路径的字典列表。
def split_pdf_by_chapters(file_path: str) -> list:
    """
    按章节拆分PDF文件
    参数:
        file_path (str): PDF文件路径
    返回:
        list: 包含章节信息和保存路径的字典列表，每个字典包含以下字段:
            - title (str): 章节标题
            - start_page (int): 章节起始页码(1-based)
            - end_page (int): 章节结束页码(1-based)
            - output_path (str): 章节PDF保存路径
    """
## 安装教程

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
项目依赖 `pymupdf`、`fastmcp` 和 `PyPDF2`，注意是`pymupdf`,不是`fitz`

可以使用以下命令安装：
```powershell
pip install pymupdf fastmcp PyPDF2
```
或者使用国内镜像源加速安装：
```powershell
pip install pymupdf fastmcp PyPDF2 -i https://pypi.tuna.tsinghua.edu.cn/simple
```
### 3. 测试程序(确保程序输出正确，可以跳过)
运行'test_main.py'文件测试程序是否正常运行：
```powershell
python test_main.py
```
如果程序正常运行，将输出：
```bash
总页数: 6

尺寸统计: [{'size': (210.01, 297.0), 'paper_type': 'A4', 'total_pages': 3, 'page_numbers': [1, 2, 6]}, {'size': (297.0, 420.0), 'paper_type': 'A3', 'total_pages': 3, 'page_numbers': [3, 4, 5]}]
```

### 4. 生成配置文件（以Trae为例）
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
## 使用说明

1.  确保已经按照安装教程完成环境配置。
2.  在'Trae'软件中，新增MCP，填入配置json内容。
3.  测试运行，确保配置正确。
- 测试1：调用mcp服务，告诉我一下这个pdf文件的页数,按打印尺寸分别统计下页数和页码.


## 注意事项

-   确保使用的是虚拟环境中的 Python 解释器，涉及到依赖问题。
-   先用纯英文目录测试，成功后再测试中文目录。
