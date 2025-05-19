import fitz
from fastmcp import FastMCP

# 创建一个 FastMCP 实例
mcp = FastMCP("PDFSizeAnalyzer-MCP")

# 定义 MCP 工具：统计 PDF 总页数
@mcp.tool()
def count_pdf_pages(file_path: str) -> int:
    """统计 PDF 总页数"""
    doc = fitz.open(file_path)
    return doc.page_count

# 定义 MCP 工具：获取每一页的尺寸（以毫米为单位）
@mcp.tool()
def get_page_dimensions(file_path: str) -> list[tuple[float, float]]:
    """获取每一页的尺寸（以毫米为单位）"""
    doc = fitz.open(file_path)
    dimensions = []
    for page in doc:
        rect = page.rect
        # 将点单位（默认 PDF 单位）转换为毫米，1 点 = 0.352777778 毫米
        width_mm = rect.width * 0.352777778
        height_mm = rect.height * 0.352777778
        # 考虑页面可能旋转的情况，交换宽高
        if page.rotation in [90, 270]:
            width_mm, height_mm = height_mm, width_mm
        dimensions.append((width_mm, height_mm))
    return dimensions

# 定义 MCP 工具：统计各尺寸纸张的数量和页码范围
@mcp.tool()
def analyze_pdf_pages(file_path: str) -> dict:
    """统计各尺寸纸张的数量和页码范围"""
    doc = fitz.open(file_path)
    dimensions = []
    for page in doc:
        rect = page.rect
        # 将点单位（默认 PDF 单位）转换为毫米，1 点 = 0.352777778 毫米
        width_mm = rect.width * 0.352777778
        height_mm = rect.height * 0.352777778
        # 考虑页面可能旋转的情况，交换宽高
        if page.rotation in [90, 270]:
            width_mm, height_mm = height_mm, width_mm
        dimensions.append((width_mm, height_mm))

    # 记录各尺寸对应的页码
    size_pages = {}
    # 对文档中实际出现的尺寸进行统计
    counts = {}
    for i, dim in enumerate(dimensions):
        # 对尺寸进行四舍五入，保留两位小数，以处理精度误差
        width, height = round(dim[0], 2), round(dim[1], 2)
        size_key = (width, height)
        if size_key in counts:
            counts[size_key] += 1
            size_pages[size_key].append(i + 1)
        else:
            counts[size_key] = 1
            size_pages[size_key] = [i + 1]
    # 定义常见尺寸映射
    common_sizes = {
        (420.0, 297.0): 'A3',
        (297.0, 210.0): 'A4',
        (210.0, 148.0): 'A5'
    }
    counts_with_description = {}
    for size_key, pages in size_pages.items():  # 处理页码范围
        pages.sort()
        ranges = []
        start = pages[0]
        end = pages[0]
        for page in pages[1:]:
            if page == end + 1:
                end = page
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f'{start}-{end}')
                start = page
                end = page
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f'{start}-{end}')
        page_ranges = ', '.join(ranges)
        description = common_sizes.get(size_key, '')
        if description:
            counts_with_description[f'{size_key} ({description})'] = {'count': counts[size_key], 'pages': page_ranges}
        else:
            counts_with_description[str(size_key)] = {'count': counts[size_key], 'pages': page_ranges}
    return counts_with_description

# 主程序：运行 MCP 服务器
if __name__ == "__main__":
    mcp.run()