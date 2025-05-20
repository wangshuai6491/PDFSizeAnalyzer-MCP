import fitz
from fastmcp import FastMCP

# 创建一个 FastMCP 实例
mcp = FastMCP("PDFSizeAnalyzer-MCP")

# 定义 MCP 工具：统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计A3A4A5常见尺寸纸张的数量和页码范围
@mcp.tool()
def analyze_pdf_pages(file_path: str) -> tuple:
    """
    统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计 A3、A4、A5 常见尺寸纸张的数量和页码范围。
    参数:
        file_path (str): 单个PDF 文件的路径。
    返回:
        tuple: 包含两个元素的元组，第一个元素是 PDF 的总页数 (int)，第二个元素是一个列表 (list)，
               列表中的每个元素是一个字典，包含纸张尺寸、纸张类型、总页数和页码范围。
    """
    doc = fitz.open(file_path)
    total_pages = doc.page_count
    dimensions = []
    size_pages = {}
    common_sizes = {
        (420.0, 297.0): 'A3',
        (297.0, 210.0): 'A4',
        (210.0, 148.0): 'A5'
    }
    # 定义误差范围
    ERROR_MARGIN = 1.0

    # 获取每一页的尺寸并处理页面旋转
    for page in doc:
        rect = page.rect
        width_mm = rect.width * 0.352777778
        height_mm = rect.height * 0.352777778
        if page.rotation in [90, 270]:
            width_mm, height_mm = height_mm, width_mm
        dimensions.append((width_mm, height_mm))

    # 统计各尺寸纸张的数量和页码范围
    for i, dim in enumerate(dimensions):
        width, height = round(dim[0], 2), round(dim[1], 2)
        # 尝试匹配常见尺寸
        paper_type = None
        for size, type in common_sizes.items():
            # 考虑横纵方向和误差范围
            if (
                (abs(width - size[0]) <= ERROR_MARGIN and abs(height - size[1]) <= ERROR_MARGIN) or
                (abs(width - size[1]) <= ERROR_MARGIN and abs(height - size[0]) <= ERROR_MARGIN)
            ):
                paper_type = type
                break

        size_key = (width, height) if paper_type is None else tuple(sorted([width, height]))
        if size_key not in size_pages:
            size_pages[size_key] = (paper_type, [])
        size_pages[size_key][1].append(i + 1)

    return total_pages, [
        {
            "size": key,
            "paper_type": value[0] if value[0] else f'Custom{int(key[0])}+{int(key[1])}',
            "total_pages": len(value[1]),
            "page_numbers": value[1]
        }
        for key, value in size_pages.items()
    ]

# 主程序：运行 MCP 服务器
if __name__ == "__main__":
    mcp.run()