import streamlit as st
from main import analyze_pdf_pages, split_pdf_by_chapters, extract_pdf_chapters, split_pdf_by_user_input, convert_pdf_to_images
import pandas as pd
from PIL import Image
import os
import tempfile
import subprocess
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, 'split_pdf_results')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

st.set_page_config(layout="wide")
st.title("📑 PDF分析")

# 侧边栏导航
with st.sidebar:
    st.header("功能导航")
    page = st.radio("选择功能", ["分析页数", "章节信息提取", "转换图片", "按页码拆分PDF", "按章节拆分"])

# 全局文件上传组件
uploaded_file = st.file_uploader("上传PDF文件", type=["pdf"], key="global_upload")

# 功能模块化
if page == "分析页数":
    if uploaded_file:
        unique_filename = os.path.join(output_dir, f'staging_{uuid.uuid4().hex}.pdf')
        with open(unique_filename, 'wb') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
        with st.spinner("正在分析PDF结构..."):
            total_pages, page_info = analyze_pdf_pages(tmp_path)
        
        st.subheader(f"📊 基础信息")
        col1, col2 = st.columns(2)
        col1.metric("总页数", total_pages)
        
        st.subheader("📐 纸张规格分布")
        df_pages = pd.DataFrame(page_info)
        format_counts = df_pages['paper_type'].value_counts().reset_index()
        format_counts.columns = ['纸张类型', '数量']
        st.bar_chart(format_counts.set_index('纸张类型'))
        
        with st.expander("🔍 详细页码分布"):
            for _, row in df_pages.iterrows():
                with st.container():
                    st.write(f"**{row['paper_type']}** ({row['size']})")
                    st.code(row['page_numbers'], language='text')

elif page == "转换图片":
    if uploaded_file:
        unique_filename = os.path.join(output_dir, f'staging_{uuid.uuid4().hex}.pdf')
        with open(unique_filename, 'wb') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
        with st.spinner("正在转换页面为图片..."):
            image_paths = convert_pdf_to_images(tmp_path)
        if image_paths:
            result_folder = os.path.dirname(image_paths[0])
            st.write(f"结果文件夹路径: {result_folder}")
            subprocess.Popen(['explorer', os.path.normpath(result_folder)])
            if st.button("打开结果文件夹"):
                subprocess.Popen(['explorer', os.path.normpath(result_folder)])
        st.subheader("✅ 转换结果")
        cols = st.columns(3)
        for idx, img_path in enumerate(image_paths[:9]):  # 最多显示9张缩略图
            with cols[idx//3]:
                img = Image.open(img_path)
                st.image(img, caption=f"第{idx+1}页", use_container_width=True)
        
elif page == "章节信息提取":
    if uploaded_file:
        unique_filename = os.path.join(output_dir, f'staging_{uuid.uuid4().hex}.pdf')
        with open(unique_filename, 'wb') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
        with st.spinner("正在解析文档结构..."):
            chapters = extract_pdf_chapters(tmp_path)
        
        if chapters:
            st.subheader("📖 文档结构")
            df_chapters = pd.DataFrame(chapters)
            # 添加下拉菜单选择标题级别
            selected_level = st.selectbox('选择标题级别', ['全部'] + sorted(df_chapters['level'].unique().tolist()))
            if selected_level != '全部':
                selected_level = int(selected_level)
                df_chapters = df_chapters[df_chapters['level'] <= selected_level]
            df_chapters['page_range'] = df_chapters['start_page'].astype(str) + '-' + df_chapters['end_page'].astype(str)
            st.dataframe(df_chapters[['level', 'title', 'page_range']], 
                                use_container_width=True)
            
            with st.expander("📂 章节详情"):
                st.json(chapters)
        else:
            st.warning("未检测到章节信息")


elif page == "按页码拆分PDF":
    if uploaded_file:
        unique_filename = os.path.join(output_dir, f'staging_{uuid.uuid4().hex}.pdf')
        with open(unique_filename, 'wb') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
        user_input = st.text_input("输入页码范围（格式：1-5,6,7-9）", "1-3")
        
        if st.button("开始拆分"):
            try:
                with st.spinner("处理中..."):
                    result = split_pdf_by_user_input(tmp_path, user_input)
                
                st.success(f"✅ 拆分为 {len(result)} 个文件")

                if result:
                    result_folder = os.path.dirname(result[0])
                    st.write(f"结果文件夹路径: {result_folder}")
                    subprocess.Popen(['explorer', result_folder])
                for file in result:
                    with st.container(border=True):
                        st.download_button(
                            label=os.path.basename(file),
                            data=open(file, 'rb').read(),
                            file_name=os.path.basename(file),
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"❌ 错误：{str(e)}")
                
elif page == "按章节拆分":
    if uploaded_file:
        unique_filename = os.path.join(output_dir, f'staging_{uuid.uuid4().hex}.pdf')
        with open(unique_filename, 'wb') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
        with st.spinner("正在解析文档结构..."):
            chapters = extract_pdf_chapters(tmp_path)
        
        if chapters:
            selected = st.multiselect("选择要拆分的章节", 
                                     [c['title'] for c in chapters],
                                     default=[chapters[0]['title']])
            
            if selected:
                with st.spinner("正在拆分选定章节..."):
                    result = split_pdf_by_chapters(tmp_path, selected)

                st.success(f"✅ 成功拆分为 {len(result)} 个文件")
                if result:
                    result_folder = os.path.dirname(result[0])
                    st.write(f"结果文件夹路径: {result_folder}")
                    subprocess.Popen(['explorer', result_folder])
                for output_file in result:
                    file_name = os.path.basename(output_file)
                    with st.container(border=True):
                        st.download_button(
                            label=f"下载 {file_name}",
                            data=open(output_file, 'rb').read(),
                            file_name=file_name,
                            mime="application/pdf"
                        )

# 底部状态栏
st.markdown("---")
st.caption("🚀 开发者模式：使用Ctrl+Shift+R强制刷新缓存")