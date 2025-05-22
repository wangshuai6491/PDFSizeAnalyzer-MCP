import unittest
from main import analyze_pdf_pages, convert_pdf_to_images, split_pdf_by_chapters

class TestAnalyzePDFPages(unittest.TestCase):
    def test_analyze_pdf_pages(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = analyze_pdf_pages(file_path)
        print('\n')
        print('总页数:', result[0])
        print('\n')
        print('尺寸统计:', result[1])
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], list)

    def test_convert_pdf_to_images(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = convert_pdf_to_images(file_path)
        print('\n')
        print('图片路径:', result)
        print('\n')
        self.assertIsInstance(result, list)
        for path in result:
            self.assertIsInstance(path, str)
            
    def test_split_pdf_by_chapters(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = split_pdf_by_chapters(file_path)
        print('\n')
        print('章节拆分结果:', result)
        print('\n')
        if result is not None:
            self.assertIsInstance(result, list)
            for chapter in result:
                self.assertIsInstance(chapter, dict)
                self.assertIn('title', chapter)
                self.assertIn('start_page', chapter)
                self.assertIn('end_page', chapter)
                self.assertIn('output_path', chapter)
    def test_extract_pdf_chapters(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = extract_pdf_chapters(file_path)
        print('\n')
        print('测试结果', result)
        
    def test_split_pdf_by_user_input(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = split_pdf_by_user_input(file_path, '1-3,4')
        print('\n')
        print('测试结果', result)
if __name__ == '__main__':
    unittest.main()