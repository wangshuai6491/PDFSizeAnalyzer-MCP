import streamlit as st
import random

# 生成随机颜色，确保不重复
def generate_unique_color(existing_colors):
    while True:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if color not in existing_colors:
            existing_colors.add(color)
            return color

# 定义卡片的 HTML 结构
def create_card(title, description, link, color):
    return f"""
    <a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
        <div style="display: flex; align-items: center; border: 1px solid #e6e6e6; border-radius: 8px; padding: 8px; margin-bottom: 8px; background-color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); cursor: pointer;">
            <div style="width: 40px; height: 40px; background-color: {color}; border-radius: 50%; margin-right: 12px;"></div>
            <div>
                <div style="font-size: 16px; font-weight: bold; color: #333;">{title}</div>
                <div style="font-size: 12px; color: #666;">{description}</div>
            </div>
        </div>
    </a>
    """

# 下面是多个网站信息
websites = [
    {"title": "开源地址", "description": "项目的开源地址", "link": "https://gitee.com/cao15110/pdfsize-analyzer-mcp"},
    {"title": "前端页面", "description": "uTools插件项目的前端页面", "link": "https://jiheutools-knvf60mx.maozi.io/"},
    {"title": "ilovepdf", "description": "免费的PDF工具", "link": "https://www.ilovepdf.com/zh-cn/compress_pdf"},
    {"title": "pdf2go", "description": "免费的PDF工具", "link": "https://www.pdf2go.com/zh/compress-pdf"},
    {"title": "谢海基", "description": "谢海基的arcgis工具箱", "link": "https://haijigiserweb-ne2vp0ok.maozi.io/"},
    {"title": "王帅", "description": "王帅的arcgis工具箱", "link": "https://share.note.youdao.com/s/5pcwelCC"},

    # 更多网站信息...
]

# 存储已使用的颜色
used_colors = set()

# 展示每个网站的卡片
cols = st.columns(4)  # 创建4列布局
for i, website in enumerate(websites):
    color = generate_unique_color(used_colors)  # 为每个卡片生成一个唯一的颜色
    with cols[i % 4]:  # 将每个卡片分配到一个列中
        st.markdown(create_card(website['title'], website['description'], website['link'], color), unsafe_allow_html=True)

# 如果网站数量不是4的倍数，需要添加空列占位
empty_cols = 4 - (len(websites) % 4)
for _ in range(empty_cols):
    with cols[(len(websites) + _) % 4]:
        st.empty()