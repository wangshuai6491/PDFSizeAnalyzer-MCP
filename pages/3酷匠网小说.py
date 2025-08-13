import requests
from lxml import etree
import streamlit as st
import threading
import zipfile
import io
from io import BytesIO

# 全局变量控制爬取状态
stop_event = threading.Event()

def getlist(url, book_id, zip_buffer, start_chapter=None, end_chapter=None):
    html = requests.get(url).text
    doc = etree.HTML(html)
    contents = doc.xpath('/html/body/div[2]/article/section/ul/li[1]/dl/dd/ol')

    if not contents:
        st.error("未找到章节内容，请检查书号是否正确！")
        return False

    total_links = len(contents[0].xpath('li/a/@href'))
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 直接在内存中创建ZIP文件
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zipf:
        processed = 0
        for i, content in enumerate(contents):
            links = content.xpath('li/a/@href')
            for j, link in enumerate(links):
                chapter_number = j + 1
                
                # 章节范围筛选
                if start_chapter and chapter_number < start_chapter:
                    continue
                if end_chapter and chapter_number > end_chapter:
                    break
                    
                if stop_event.is_set():
                    status_text.warning("爬取已停止！")
                    progress_bar.empty()
                    return True
                
                full_url = 'http://www.kujiang.com' + link
                try:
                    html_content = requests.get(full_url, timeout=10).text
                except requests.exceptions.RequestException as e:
                    st.error(f"获取章节内容失败: {e}")
                    continue
                    
                doc = etree.HTML(html_content)
                title = doc.xpath('/html/body/article/div[2]/div[2]/div[1]/h1/text()')
                contents_xpath = doc.xpath('/html/body/article/div[2]/div[2]/div[3]/div[1]')
                
                if not title or not contents_xpath:
                    st.warning(f"章节结构异常，跳过: {full_url}")
                    continue
                    
                # 构建章节内容
                chapter_content = []
                for para in contents_xpath[0].xpath('p/text()'):
                    chapter_content.append(para)
                
                # 直接写入内存中的ZIP文件
                file_name = f"{title[0].replace('/', '_')}.txt"  # 处理特殊字符
                zipf.writestr(file_name, '\n'.join(chapter_content).encode('utf-8'))
                
                # 更新进度
                processed += 1
                progress = processed / min(total_links, (end_chapter or total_links) - (start_chapter or 0))
                progress_bar.progress(min(progress, 1.0))
                status_text.info(f"已处理: {title[0]} ({processed}/{min(total_links, (end_chapter or total_links))})")
                
    status_text.success("爬取完成！")
    progress_bar.empty()
    return True

def main():
    global stop_event
    stop_event.clear()
    
    st.title("酷匠小说网小说爬取工具")
    st.markdown("[酷匠小说网](http://www.kujiang.com/) 请输入小说的书号，例如www.kujiang.com/book/67371中的67371就是书号：")
    
    urlsh = st.text_input("请输入书号：")
    zip_buffer = BytesIO()  # 创建内存缓冲区
    st.session_state['zip_buffer'] = zip_buffer
    
    st.write("爬取指定章节的小说（可选）：")
    col1, col2 = st.columns(2)
    with col1:
        start_chapter = st.number_input("起始章节：", min_value=1, value=1, step=1)
    with col2:
        end_chapter = st.number_input("结束章节：", min_value=start_chapter, value=start_chapter, step=1)
    
    col3, col4 = st.columns(2)
    if col3.button("开始爬取"):
        if not urlsh:
            st.error("请输入书号！")
            return
            
        st.session_state['zip_buffer'] = BytesIO()  # 重置缓冲区
        url = f"http://www.kujiang.com/book/{urlsh}/catalog"
        st.write(f"正在爬取小说：{url}")
        
        with st.spinner("正在爬取章节内容..."):
            success = getlist(
                url, 
                urlsh, 
                st.session_state['zip_buffer'], 
                start_chapter if start_chapter > 1 else None,
                end_chapter if end_chapter > 1 else None
            )
            
        if success:
            st.session_state['zip_buffer'].seek(0)  # 将指针移到缓冲区开头
    
    if col4.button("停止爬取"):
        stop_event.set()
        st.warning("正在停止爬取...")
    
    # 下载按钮
    if 'zip_buffer' in st.session_state and st.session_state['zip_buffer'].getbuffer().nbytes > 0:
        st.download_button(
            label="下载小说压缩包",
            data=st.session_state['zip_buffer'],
            file_name=f"book_{urlsh}.zip",
            mime="application/zip"
        )

if __name__ == '__main__':
    main()