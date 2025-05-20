import unittest
from main import analyze_pdf_pages

class TestAnalyzePDFPages(unittest.TestCase):
    def test_analyze_pdf_pages(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿.pdf'
        result = analyze_pdf_pages(file_path)
        print('\n')
        print('总页数:', result[0])
        print('\n')
        print('尺寸统计:', result[1])
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], list)

if __name__ == '__main__':
    unittest.main()