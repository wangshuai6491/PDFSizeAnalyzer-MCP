import unittest
from main import split_pdf_by_user_input

class TestAnalyzePDFPages(unittest.TestCase):
    def test_split_pdf_by_user_input(self):
        # 请替换为实际的 PDF 文件路径
        file_path = '测试文稿\\测试文稿.pdf'
        result = split_pdf_by_user_input(file_path, '1-3,4')
        print('\n')
        print('测试结果', result)
if __name__ == '__main__':
    unittest.main()