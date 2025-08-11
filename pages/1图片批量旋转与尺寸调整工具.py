# app.py
import os
import streamlit as st
from PIL import Image
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import tkinter as tk
from tkinter import filedialog
import platform
import webbrowser

# -------------------- 业务逻辑 --------------------
# 统一资源打开方法
def open_explorer(path):
    path = os.path.normpath(path)
    if platform.system() == 'Windows':
        webbrowser.open(f'file:///{path}')
    elif platform.system() == 'Darwin':  # macOS
        webbrowser.open(f'file://{path}')
    else:  # Linux
        webbrowser.open(f'file://{path}')

def process_images(
        input_dir,
        rotation_angle,
        target_width,
        target_height,
        lock_aspect_ratio=False,
        process_subfolders=False,
        target_dpi=300,
        preserve_exif=True,
        progress=None
):
    """
    与原脚本 process_images 完全一致，只把日志/进度输出改为 Streamlit 的 progress 与 st.text
    """
    processed_count = 0
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif',
                         '.bmp', '.tiff', '.webp')
    output_base_dir = os.path.join(input_dir, 'processed_images')
    os.makedirs(output_base_dir, exist_ok=True)

    tasks = []

    def collect_tasks(current_dir):
        for entry in os.scandir(current_dir):
            if entry.is_file() and entry.name.lower().endswith(supported_formats):
                tasks.append(entry.path)
            elif entry.is_dir() and process_subfolders and entry.name != 'processed_images':
                collect_tasks(entry.path)

    collect_tasks(input_dir)
    total = len(tasks)
    if total == 0:
        st.warning("未找到任何支持的图片文件。")
        return 0

    bar = progress or st.progress(0)

    def handle_one(path):
        nonlocal processed_count
        try:
            with Image.open(path) as img:
                exif = img.info.get('exif')
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                if rotation_angle != 0:
                    img = img.rotate(-rotation_angle, expand=True)

                if lock_aspect_ratio:
                    img.thumbnail((target_width, target_height),
                                  Image.Resampling.LANCZOS)
                else:
                    img = img.resize(
                        (target_width, target_height), Image.Resampling.LANCZOS)

                rel = os.path.relpath(path, input_dir)
                out_path = os.path.join(output_base_dir, rel)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)

                save_kwargs = {'dpi': (target_dpi, target_dpi)}
                if preserve_exif and exif and out_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs['exif'] = exif
                    save_kwargs['quality'] = 95
                    save_kwargs['optimize'] = True
                elif out_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs['quality'] = 95
                    save_kwargs['optimize'] = True
                elif out_path.lower().endswith('.png'):
                    save_kwargs['optimize'] = True

                img.save(out_path, **save_kwargs)
                processed_count += 1
                bar.progress(min(processed_count / total, 1.0))
                return True
        except Exception as e:
            st.error(f"处理失败 {os.path.basename(path)} : {e}")
            return False

    with ThreadPoolExecutor() as pool:
        list(pool.map(handle_one, tasks))

    return processed_count

# 处理文件夹选择

def pick_folder() -> str:
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)   # 置顶
    path = filedialog.askdirectory(master=root)
    root.destroy()
    return path

# --------------------开始绘制页面 Streamlit UI --------------------
st.set_page_config(page_title="图片批量旋转与尺寸调整工具",page_icon="🖼️", layout="centered")
st.title("🖼️ 图片批量旋转与尺寸调整工具")
# 样式——按钮居中
st.markdown('<style>div.stButton>button{display:block;margin:0 auto}</style>', unsafe_allow_html=True)

# 选择文件夹
if st.button("📁 选择文件夹"):
    folder = pick_folder()
    if folder:
        st.session_state.folder = folder
        st.rerun()

folder = st.session_state.get("folder", "")
# 用户可直接输入文件夹路径
folder = st.text_input("已选文件夹（可手动粘贴文件夹路径，回车确认）", folder, key="folder_display")

if folder:
    # 旋转角度
    rotate = st.radio("旋转角度",
                    options=[0, 90, 180, 270],
                    format_func=lambda x: {0: "不旋转",
                                            90: "顺时针 90°",
                                            180: "180°",
                                            270: "逆时针 90°"}[x],
                    horizontal=True)

    # 尺寸设置
    col1, col2 = st.columns(2)
    width = col1.number_input("宽度", value=10.0, min_value=0.1, step=0.1)
    height = col2.number_input("高度", value=15.0, min_value=0.1, step=0.1)

    unit = st.radio("单位", options=["厘米", "像素"], horizontal=True)
    dpi = st.selectbox("DPI（仅厘米单位生效）",
                    options=[72, 96, 150, 300, 600], index=3)

    lock_aspect = st.checkbox("锁定纵横比", value=True)
    subfolders = st.checkbox("处理子文件夹", value=True)
    office_optimize = st.checkbox("为办公软件优化（WPS/Word 等）", value=True)
    preserve_exif = st.checkbox("保留 EXIF 信息")


    # 转换为目标像素
    if st.button("开始处理", type="primary"):
        if not folder or not os.path.isdir(folder):
            st.error("请输入有效的文件夹路径！")
            st.stop()

        if unit == "厘米":
            target_w = int(round(width * dpi / 2.54))
            target_h = int(round(height * dpi / 2.54))
            st.info(f"尺寸换算：{width}×{height} cm → {target_w}×{target_h} px")
        else:
            target_w, target_h = int(width), int(height)

        final_dpi = dpi if office_optimize else 96

        progress = st.progress(0)
        start = time.time()
        count = process_images(folder, rotate, target_w, target_h,
                            lock_aspect, subfolders, final_dpi, preserve_exif, progress)
        elapsed = time.time() - start

        result_folder = os.path.join(folder, 'processed_images')
        st.success(f"✅ 处理完成！共 {count} 张图片，耗时 {elapsed:.1f}s\n"
                f"结果保存在：{result_folder}")
        open_explorer(result_folder)
# 底部状态栏
st.markdown("---")
st.caption("🚀 页面缓存可通过 Ctrl+Shift+R 强制刷新")
st.caption("🚀 开发者：谢海基，集成打包：王帅")