import fitz  # PyMuPDF
import os


# 示例用法
if __name__ == "__main__":
    pdf_path = r"E:\trae\mcp\pdfsize-analyzer-mcp\测试文稿\0522.pdf"
    user_input = input("请输入页码范围（如1-5,6,7-9,9-12）：")
    
    try:
        output_files = split_pdf_by_user_input(pdf_path, user_input)
        print("PDF分割完成！输出文件：")
        for file in output_files:
            print(file)
    except Exception as e:
        print(f"处理PDF时发生错误: {e}")