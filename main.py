# -*- coding: utf-8 -*- 
import fitz
from fastmcp import FastMCP
import os
from PyPDF2 import PdfReader, PdfWriter

# 创建一个 FastMCP 实例
mcp = FastMCP("PDFSizeAnalyzer-MCP")

# 定义 MCP 工具：统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计A3A4A5常见尺寸纸张的数量和页码范围
@mcp.tool()
def analyze_pdf_pages(file_path: str) -> tuple:
    """
    统计 PDF 总页数，获取每一页的尺寸（以毫米为单位），同时统计 A3、A4等常见尺寸纸张的数量和页码范围。
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
        (210.0, 148.0): 'A5',
        (841.0, 1189.0): 'A0',
        (594.0, 841.0): 'A1',
        (420.0, 594.0): 'A2',
        (148.0, 105.0): 'A6',
        (105.0, 74.0): 'A7',
        (74.0, 52.0): 'A8',
        (52.0, 37.0): 'A9',
        (37.0, 26.0): 'A10',
        (364.0, 257.0): 'B3',
        (257.0, 182.0): 'B4',
        (182.0, 128.0): 'B5',
        (128.0, 91.0): 'B6',
        (91.0, 64.0): 'B7',
        (64.0, 45.0): 'B8',
        (45.0, 32.0): 'B9',
        (32.0, 23.0): 'B10',
        (215.9, 279.4): 'Letter',
        (279.4, 431.8): 'Legal',
        (215.9, 355.6): 'Tabloid'
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

    def merge_page_numbers(pages):
        if not pages:
            return ""
        pages_sorted = sorted(pages)
        ranges = []
        start = end = pages_sorted[0]
        for page in pages_sorted[1:]:
            if page == end + 1:
                end = page
            else:
                ranges.append(f"{start}-{end}" if start != end else f"{start}")
                start = end = page
        ranges.append(f"{start}-{end}" if start != end else f"{start}")
        return ", ".join(ranges)

    # 合并相同纸张类型的页码
    merged_results = {}
    for key, value in size_pages.items():
        paper_type = value[0] if value[0] else f'Custom{int(key[0])}+{int(key[1])}'
        if paper_type not in merged_results:
            merged_results[paper_type] = {
                "size": key,
                "paper_type": paper_type,
                "total_pages": 0,
                "page_numbers": []
            }
        merged_results[paper_type]["total_pages"] += len(value[1])
        merged_results[paper_type]["page_numbers"] += value[1]
    
    # 对合并后的页码进行排序和范围合并
    for result in merged_results.values():
        result["page_numbers"] = merge_page_numbers(result["page_numbers"])
    
    return total_pages, list(merged_results.values())

# 定义 MCP 工具：将 PDF 的每一页转换为图片，并保存到以 PDF 名称命名的文件夹中。
@mcp.tool()
def convert_pdf_to_images(file_path: str)-> list:
    """
    将 PDF 的每一页转换为图片，并保存到以 PDF 名称命名的文件夹中。
    参数:
        file_path (str): 单个 PDF 文件的路径。
    返回:
        list: 包含所有生成图片文件路径的列表。
    """
    import os
    from pathlib import Path
    doc = fitz.open(file_path)
    pdf_name = Path(file_path).stem
    output_folder = Path(os.getcwd()) / pdf_name
    output_folder.mkdir(parents=True, exist_ok=True)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image_path = output_folder / f'{pdf_name}_page{page_num + 1}.png'
        pix.save(str(image_path))
        image_paths.append(str(image_path))
    return image_paths

# 定义 MCP 工具：压缩PDF文件，将PDF文件转换为图片型PDF，通过控制图片质量1-100实现体积压缩
@mcp.tool()
def compress_pdf(file_path: str, quality: int = 75) -> str:
    """
    PDF文件压缩(图片型)
    
    参数:
        file_path: PDF文件路径
        quality: 压缩质量 (0-100)
    
    返回:
        str: 压缩后的PDF文件路径
    """
    doc = fitz.open(file_path)

    pdf_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(os.path.dirname(file_path), f"{pdf_name}_图片型_压缩质量{quality}.pdf")
    
    # 创建新的PDF文档
    new_doc = fitz.open()
    
    # 逐页处理
    for page in doc:
        # 获取页面内容作为图像，应用质量参数
        pix = page.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), 
                            colorspace=fitz.csRGB, 
                            clip=None, 
                            alpha=False, 
                            annots=True,
                            dpi=int(72 * (quality/100)))
        # 创建新页面并插入压缩后的图像
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, pixmap=pix, keep_proportion=True)
    
    # 保存压缩后的PDF
    new_doc.save(output_path, deflate=True, garbage=4, clean=True)
    new_doc.close()
    doc.close()
    
    return output_path

# 定义 MCP 工具：压缩PDF文件，通过删除不必要的元素实现体积压缩
@mcp.tool()
def optimize_pdf(file_path: str) -> str:
    """
    PDF优化压缩(文本保留型)
    
    参数:
        file_path: PDF文件路径
    
    返回:
        str: 优化后的PDF文件路径
    """
    doc = fitz.open(file_path)
    
    pdf_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(os.path.dirname(file_path), f"{pdf_name}_优化压缩.pdf")
    
    # 保存优化后的PDF
    doc.save(output_path, 
            garbage=4,  # 移除未引用对象
            deflate=True,  # 压缩流
            clean=True,  # 清理文档结构
            linear=True,  # 线性化PDF
            deflate_fonts=True,  # 压缩字体
            deflate_images=True)  # 压缩图像
    
    doc.close()
    return output_path

# 定义 MCP 工具：获取所有章节（书签）信息
@mcp.tool()
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
    chapters = []
    doc = fitz.open(file_path)
    
    # 获取PDF的所有书签
    toc = doc.get_toc()
    
    if not toc:
        print("此PDF文件没有书签信息")
        return []
    
    # 解析书签结构
    for entry in toc:
        # entry格式为：[层级, 标题, 页码, ...]
        level, title, page_num = entry[0], entry[1], entry[2]
        
        # 处理起始页码（fitz的页码从0开始，普通书籍从1开始）
        start_page = page_num
        
        # 添加到章节列表
        chapters.append({
            'level': level,
            'title': title,
            'start_page': start_page
        })
    
    # 确定每个章节的结束页码
    total_pages = doc.page_count
    for i in range(len(chapters)):
        current_chapter = chapters[i]
        
        # 如果是最后一个章节，结束页码是PDF的最后一页
        if i == len(chapters) - 1:
            current_chapter['end_page'] = total_pages
        else:
            # 否则，结束页码是下一个相同层级章节的起始页码减1
            next_chapter = chapters[i + 1]
            while next_chapter['level'] > current_chapter['level']:
                # 如果下一个章节是子章节，继续查找同级的下一个章节
                if i + 1 >= len(chapters) - 1:
                    # 如果是最后一个章节，结束页码是PDF的最后一页
                    current_chapter['end_page'] = total_pages
                    break
                i += 1
                next_chapter = chapters[i + 1]
                
                # 防止无限循环
                if i >= len(chapters) - 1:
                    current_chapter['end_page'] = total_pages
                    break
            
            if 'end_page' not in current_chapter:
                current_chapter['end_page'] = next_chapter['start_page'] - 1
    
    doc.close()
    return chapters

# 定义 MCP 工具：根据用户输入的页码范围将PDF分隔成多个单独的PDF文件。
@mcp.tool()
def split_pdf_by_user_input(file_path: str, user_input: str) -> list:
    """
    根据用户输入的页码范围将PDF分隔成多个单独的PDF文件。

    Args:
        file_path: 要分割的PDF文件路径。
        user_input: 用户输入的页码范围，如"1-5,6,7-9,9-12"。

    Returns:
        分割后的PDF文件路径列表。
    """
    # 解析用户输入的页码范围
    def parse_page_input(user_input):
        page_ranges = []
        parts = user_input.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                if start > end:
                    raise ValueError(f"无效的页码范围：{part}")
                page_ranges.append((start, end))
            else:
                page_num = int(part)
                page_ranges.append((page_num, page_num))
        return page_ranges

    # 保存PDF的指定页面到新文件
    def save_pages(doc, start_index, end_index, output_path):
        output_doc = fitz.open()
        output_doc.insert_pdf(doc, from_page=start_index, to_page=end_index)
        output_doc.save(output_path)
        output_doc.close()

    page_ranges = parse_page_input(user_input)
    
    # 验证页码范围
    doc = fitz.open(file_path)
    total_pages = doc.page_count
    for page_range in page_ranges:
        start_page, end_page = page_range
        if start_page < 1 or end_page > total_pages:
            raise ValueError(f"页码超出范围，PDF共{total_pages}页")
    
    # 创建输出目录
    output_dir = os.path.splitext(file_path)[0] + "_split"
    os.makedirs(output_dir, exist_ok=True)
    
    # 分割PDF并保存
    output_files = []
    for i, (start_page, end_page) in enumerate(page_ranges, 1):
        output_file = os.path.join(output_dir, f"part_{i}_{start_page}-{end_page}.pdf")
        # fitz的页码从0开始，所以需要减1
        save_pages(doc, start_page - 1, end_page - 1, output_file)
        output_files.append(output_file)
    
    doc.close()
    return output_files

# 定义 MCP 工具：按章节拆分 PDF 文件，支持选择拆分的章节。
@mcp.tool()
def split_pdf_by_chapters(file_path: str, selected_chapters=None) -> list:
    """
    根据用户选择的章节拆分PDF文件。

    参数:
        file_path (str): PDF文件的路径。
        selected_chapters (list, 可选): 要拆分的章节列表。如果为None，则拆分所有章节。

    返回:
        list: 包含所有拆分后PDF文件路径的列表。
    """
    if selected_chapters is None:
        chapters = extract_pdf_chapters(file_path)
    else:
        all_chapters = extract_pdf_chapters(file_path)
        chapters = [chapter for chapter in all_chapters if chapter['title'] in selected_chapters]

    split_files = []
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(os.path.dirname(file_path), base_name)
    os.makedirs(output_dir, exist_ok=True)
    for chapter in chapters:
        start_page = chapter['start_page'] - 1
        end_page = chapter['end_page']
        reader = PdfReader(file_path)
        writer = PdfWriter()
        for page_num in range(start_page, end_page):
            writer.add_page(reader.pages[page_num])

        chapter_title = chapter['title'].replace(' ', '_').replace('/', '_')
        output_file = os.path.join(output_dir, f'{chapter_title}.pdf')
        with open(output_file, 'wb') as out_file:
            writer.write(out_file)
        split_files.append(output_file)

    return split_files

# 主程序：运行 MCP 服务器
if __name__ == "__main__":
    mcp.run()
