import streamlit as st
import wx

# 初始化 Streamlit 页面
st.set_page_config(page_title="文件夹选择示例", layout="centered")
st.title("文件夹选择示例")

# 定义一个函数来创建文件夹选择对话框
def select_folder():
    app = wx.App()
    dialog = wx.DirDialog(None, "选择文件夹：", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        folder_path = dialog.GetPath()
        dialog.Destroy()
        app.Destroy()
        return folder_path
    else:
        dialog.Destroy()
        app.Destroy()
        return None

# 创建一个按钮
if st.button("浏览"):
    folder_path = select_folder()
    if folder_path:
        st.write(f"选定的文件夹路径: {folder_path}")
    else:
        st.write("未选择任何文件夹")