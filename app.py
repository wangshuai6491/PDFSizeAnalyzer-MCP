import streamlit as st
import pandas as pd
from PIL import Image
import os
import tempfile
import platform
import webbrowser
from contextlib import contextmanager
from main import (
    analyze_pdf_pages,
    split_pdf_by_chapters,
    extract_pdf_chapters,
    split_pdf_by_user_input,
    convert_pdf_to_images
)

# 初始化配置
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, 'split_pdf_results')
os.makedirs(output_dir, exist_ok=True)

# 自定义上下文管理器用于临时文件
def create_temp_file(suffix='', prefix='tmp'):
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=output_dir)
        os.close(fd)  # 立即关闭文件描述符
        return path

# 统一文件上传处理

def handle_file_upload():
    uploaded_file = st.file_uploader("上传PDF文件", type=["pdf"], key="global_upload")
    if uploaded_file:
        original_filename = uploaded_file.name
        tmp_path = os.path.join(output_dir, original_filename)
        with open(tmp_path, 'wb') as f:
            f.write(uploaded_file.read())
        st.session_state.tmp_path = tmp_path  # 存储到session保持引用
        return True
    return False

# 统一资源打开方法
def open_explorer(path):
    path = os.path.normpath(path)
    if platform.system() == 'Windows':
        webbrowser.open(f'file:///{path}')
    elif platform.system() == 'Darwin':  # macOS
        webbrowser.open(f'file://{path}')
    else:  # Linux
        webbrowser.open(f'file://{path}')

# 页面配置
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title("📑 PDF分析工具")

# 侧边栏导航
with st.sidebar:
    st.header("功能导航")
    page = st.radio("选择功能", ["分析页数", "章节信息提取", "转换图片", "按页码拆分PDF", "按章节拆分"])

# 主内容区
if page == "分析页数":
    tmp_path = None
    if handle_file_upload(): 
        tmp_path = st.session_state.tmp_path
        try:
            with st.spinner("正在分析PDF结构..."):
                total_pages, page_info = analyze_pdf_pages(tmp_path)
            st.subheader(f"📊 基础信息")
            col1, col2 = st.columns(2)
            col1.metric("总页数", total_pages)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    st.warning(f"删除临时文件时出错: {e}")
        
        # 优化图表显示
        df_pages = pd.DataFrame(page_info)
        if not df_pages.empty:
            format_counts = df_pages['paper_type'].value_counts().reset_index()
            format_counts.columns = ['纸张类型', '数量']
            with st.expander("📐 纸张规格分布"):
                st.bar_chart(format_counts.set_index('纸张类型'))
            
            # 分页显示详细信息
            with st.expander("🔍 详细页码分布"):
                page_chunk = st.empty()
                for i, (_, row) in enumerate(df_pages.iterrows()):
                    if i > 0 and i % 10 == 0:
                        page_chunk.write("...")
                        if st.button("显示更多", key=f"show_more_{i}"):
                            continue
                    with st.container():
                        st.write(f"**{row['paper_type']}** ({row['size']})")
                        st.code(row['page_numbers'], language='text')

elif page == "转换图片":
    if handle_file_upload():
        with st.spinner("正在转换页面为图片..."):
            image_paths = convert_pdf_to_images(st.session_state.tmp_path)
        
        if image_paths:
            result_folder = os.path.dirname(image_paths[0])
            st.success(f"✅ 转换完成，共生成 {len(image_paths)} 张图片,结果文件夹路径: {result_folder}")
            open_explorer(result_folder)
            
            # 优化图片显示
            cols = st.columns(3)
            for idx, img_path in enumerate(image_paths[:9]):
                with cols[idx//3]:
                    with Image.open(img_path) as img:
                        st.image(img, use_container_width=True)

elif page == "章节信息提取":
    if handle_file_upload():
        with st.spinner("正在解析文档结构..."):
            chapters = extract_pdf_chapters(st.session_state.tmp_path)
        
        if chapters:
            df_chapters = pd.DataFrame(chapters)
            # 改进筛选器
            level_options = ['全部'] + sorted(df_chapters['level'].unique().astype(str))
            selected_level = st.selectbox('选择标题级别', level_options)
            
            if selected_level != '全部':
                df_chapters = df_chapters[df_chapters['level'] <= int(selected_level)]
            
            # 优化表格显示
            st.subheader("📖 文档结构")
            format_df = df_chapters.copy()
            format_df['page_range'] = format_df.apply(
                lambda x: f"{x.start_page}-{x.end_page}", axis=1)
            st.dataframe(format_df[['level', 'title', 'page_range']], use_container_width=True, hide_index=True)
            
            # 优化JSON显示
            with st.expander("📂 章节详情"):
                st.json(chapters)
        else:
            st.warning("⚠️ 未检测到章节信息")

elif page == "按页码拆分PDF":
    if handle_file_upload():
        user_input = st.text_input("输入页码范围（格式：1-5,6,7-9）", "1-3")
        if st.button("开始拆分"):
            try:
                with st.spinner("处理中..."):
                    result = split_pdf_by_user_input(st.session_state.tmp_path, user_input)
                
                # 改进结果展示
                with st.success(f"✅ 成功拆分为 {len(result)} 个文件"):
                    result_dir = os.path.dirname(result[0])
                    open_explorer(result_dir)
                    
                    # 优化下载方式
                    for file in result:
                        with st.container(border=True):
                            with open(file, 'rb') as f:
                                btn = st.download_button(
                                    label=os.path.basename(file),
                                    data=f.read(),
                                    file_name=os.path.basename(file),
                                    mime="application/pdf",
                                    key=file
                                )
            except ValueError as ve:
                st.error(f"❌ 输入格式错误：{str(ve)}")
            except Exception as e:
                st.error(f"❌ 处理失败：{str(e)}")

elif page == "按章节拆分":
    if handle_file_upload():
        with st.spinner("正在解析文档结构..."):
            chapters = extract_pdf_chapters(st.session_state.tmp_path)
        
        if chapters:
            all_options = [c['title'] for c in chapters]
            selected = st.multiselect("选择要拆分的章节", all_options)
            if selected:
                st.write(f"已选择：{len(selected)} 个项目")
                for item in selected:
                    st.write(f"- {item}")
            select_all = st.checkbox("全选")
            if select_all:
                selected = [c['title'] for c in chapters]
            split_button = st.button("开始拆分")
            if split_button and selected:
                with st.spinner("正在拆分选定章节..."):
                    try:
                        result = split_pdf_by_chapters(st.session_state.tmp_path, selected)
                        
                        with st.success(f"✅ 成功拆分为 {len(result)} 个文件"):
                            result_dir = os.path.dirname(result[0])
                            open_explorer(result_dir)
                            
                            for file in result:
                                with st.container(border=True):
                                    with open(file, 'rb') as f:
                                        btn = st.download_button(
                                            label=os.path.basename(file),
                                            data=f.read(),
                                            file_name=os.path.basename(file),
                                            mime="application/pdf",
                                            key=file
                                        )
                    except Exception as e:
                        st.error(f"❌ 拆分失败：{str(e)}")

# 底部状态栏
st.markdown("---")
st.caption("🚀 开发者提示：页面缓存可通过 Ctrl+Shift+R 强制刷新")
