import requests
from lxml import etree
import streamlit as st
import os
import threading

# 全局变量，用于控制爬取程序的运行状态
stop_event = threading.Event()

# 1 获取超链接
def getlist(url, book_id, start_chapter=None, end_chapter=None):
    html = requests.get(url).text  # 用get的方式去访问这个网站

    # 2 提取超链接
    doc = etree.HTML(html)  # 用etree.HTML()的方式去构造xpath解析对象
    contents = doc.xpath('/html/body/div[2]/article/section/ul/li[1]/dl/dd/ol')

    # 创建以书号为命名的文件夹
    folder_name = f"book_{book_id}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    total_links = len(contents[0].xpath('li/a/@href')) if contents else 0
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, content in enumerate(contents):
        links = content.xpath('li/a/@href')
        for j, link in enumerate(links):
            chapter_number = j + 1

            # 检查章节范围
            if start_chapter is not None and chapter_number < start_chapter:
                continue
            if end_chapter is not None and chapter_number > end_chapter:
                break

            if stop_event.is_set():  # 检查是否点击了停止按钮
                status_text.warning("爬取已停止！")
                progress_bar.empty()
                return

            full_url = 'http://www.kujiang.com' + link
            html = requests.get(full_url).text
            doc = etree.HTML(html)
            title = doc.xpath('/html/body/article/div[2]/div[2]/div[1]/h1/text()')
            contents = doc.xpath('/html/body/article/div[2]/div[2]/div[3]/div[1]')

            # 3 保存txt到指定文件夹
            file_path = os.path.join(folder_name, f'{title[0]}.txt')
            with open(file_path, 'w', encoding='utf-8') as f:
                for neirong in contents:
                    content = neirong.xpath('p/text()')
                    for items in content:
                        f.write(items)
                        f.write('\n')

            # 更新进度条和状态信息
            progress = (i * len(links) + j + 1) / total_links
            progress_bar.progress(progress)
            status_text.info(f"正在爬取：{title[0]} ({i * len(links) + j + 1}/{total_links})")

    status_text.success("爬取完成！")
    progress_bar.empty()

# Streamlit界面
def main():
    global stop_event
    stop_event.clear()  # 重置停止事件

    # 设置页面标题和副标题
    st.title("酷匠小说网小说爬取工具")
    st.markdown("[酷匠小说网](http://www.kujiang.com/) 请输入小说的书号，例如www.kujiang.com/book/67371中的67371就是书号：")

    # 输入框
    urlsh = st.text_input("请输入书号：")
    st.write("爬取指定章节的小说，请输入起始章节和结束章节（可选），不输入则默认爬取全部章节：")
    col1, col2 = st.columns(2)  # 创建两列
    with col1:
        start_chapter = st.number_input("请输入起始章节（可选）：", min_value=1, value=1, step=1)
    with col2:
        end_chapter = st.number_input("请输入结束章节（可选）：", min_value=start_chapter, value=start_chapter, step=1)

    # 按钮
    col3, col4 = st.columns(2)  # 创建两列
    if col3.button("开始爬取"):
        if urlsh:
            url = f'http://www.kujiang.com/book/{urlsh}/catalog'
            st.write(f"正在爬取小说：{url}")
            getlist(url, urlsh, start_chapter if start_chapter > 1 else None, end_chapter if end_chapter > 1 else None)
            st.success(f"爬取完成！小说已保存到文件夹：book_{urlsh}")
        else:
            st.error("请输入书号！")

    if col4.button("停止爬取"):
        stop_event.set()  # 设置停止事件
        st.warning("正在尝试停止爬取...")

if __name__ == '__main__':
    main()