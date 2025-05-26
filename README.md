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

### 3.根据用户选择的章节拆分PDF文件，返回保存路径的字典列表。

def split_pdf_by_chapters(file_path: str, selected_chapters=None) -> list:
    """
    根据用户选择的章节拆分PDF文件。

    参数:
        file_path (str): PDF文件的路径。
        selected_chapters (list, 可选): 要拆分的章节列表。如果为None，则拆分所有章节。

    返回:
        list: 包含所有拆分后PDF文件路径的列表。
    """

### 4.从PDF中提取章节标题及其起始和结束页码。

def extract_pdf_chapters(file_path: str)-> list:
    """
    从PDF中提取章节标题及其起始和结束页码。

    参数:
        file_path: PDF文件路径

    返回:
        chapters: 列表，每个元素是一个字典，包含章节信息
            - level: 章节的层级（例如，1级书签、2级书签等）。层级越低，章节越重要或越靠上。
            - title: 章节的标题。
            - start_page: 章节的起始页码。
            - end_page: 章节的结束页码。
    """

### 5.根据用户输入的页码范围将PDF分隔成多个单独的PDF文件。

def split_pdf_by_user_input(file_path: str, user_input: str) -> list:
    """
    根据用户输入的页码范围将PDF分隔成多个单独的PDF文件。

    Args:
        file_path: 要分割的PDF文件路径。
        user_input: 用户输入的页码范围，如"1-5,6,7-9,9-12"。

    Returns:
        分割后的PDF文件路径列表。
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

可以使用以下命令安装：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 测试程序(确保程序输出正确，可以跳过)

运行'test_main.py'文件测试程序是否正常运行：

```powershell
python test_main.py
```

如果程序正常运行，将输出：

```bash
Ran 这里是mcp的数量 tests in 时间s

OK
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

### mcp使用说明

1. 确保已经按照安装教程完成环境配置。
2. 在'Trae'软件中，新增MCP，填入配置json内容。
3. 测试运行，确保配置正确。

- 测试1：调用mcp服务，告诉我一下这个pdf文件的页数,按打印尺寸分别统计下页数和页码.

### 本地浏览器使用说明

1. 用streamlit运行app.py

```bash
.\venv\Scripts\activate
streamlit run app.py --server.port 8501
```

2. 根据运行窗口生成的网址，或自动打开的网址，在浏览器中打开。
3. 上传pdf文件，根据需求点击按钮，结果展示在网页展示，并自动打开结果文件夹。

## pyinsaller打包教程

1. 激活虚拟环境

```bash
.\venv\Scripts\activate
```

2. 用spec打包，注意打包streamlit有点不同：

需要额外的run_app.py文件，需要特定的文件夹hooks，这个文件夹内还需要特定的hook-streamlit.py。
当然这些文件的内容都是固定的，不需要自己修改。

有了上面的基础，就可以打包了。
```bash
pyinstaller run_app.spec
```

3. 打包完成后，在 dist 目录下会生成一个可执行文件,但这个执行文件无法运行，还需要把依赖的py文件复制到dist目录下。
本项目中是：
app.py # 前端主程序
main.py # 后端主程序

## 注意事项

- 确保使用的是虚拟环境中的 Python 解释器，涉及到依赖问题。
- 先用纯英文目录测试，成功后再测试中文目录。
