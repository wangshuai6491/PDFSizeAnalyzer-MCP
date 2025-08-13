import requests
import re
import os
import time
import streamlit as st

# 下载单首歌曲代码
def GETXIAZAI(url, name, progress_bar, progress_text):
    houzhui = url[-4:]
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        total_size = int(res.headers.get('content-length', 0))
        downloaded_size = 0
        progress_bar.progress(0)
        progress_text.text(f"正在下载: {name}...")

        with open(f'{name}{houzhui}', 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    progress = int((downloaded_size / total_size) * 100)
                    progress_bar.progress(progress)

        progress_text.text(f"下载完成: {name}")
        return True
    else:
        progress_text.text(f"下载失败: {name} (状态码: {res.status_code})")
        return False

# 获取歌单中的所有音乐名字和下载链接地址
def getAllMusicList(play_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'application/json, text/javascript',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://music.163.com',
        'Connection': 'keep-alive',
        'Referer': 'https://music.163.com/playlist?id=2566843552',
        'TE': 'Trailers',
    }

    # 获取页面内容
    response = requests.get(play_url, headers=headers).text

    # 使用正则表达式匹配出对应的歌曲名称和地址
    pattern = re.compile(r'<a href="/song\?id=(\d+)">(.*?)</a>')
    matches = pattern.findall(response)

    lists = []
    for music_id, music_name in matches:
        musicUrl = f'http://music.163.com/song/media/outer/url?id={music_id}.mp3'
        lists.append([music_name, musicUrl])

    return lists

# 下载歌单lists中的所有音乐
def downloadMusicList(lists):
    ticks = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    folder_name = f'music_{ticks}'
    os.mkdir(folder_name)

    total_songs = len(lists)
    progress_bar = st.progress(0)
    progress_text = st.empty()

    for index, i in enumerate(lists):
        url = i[1]
        name = i[0]
        try:
            st.write(f'正在下载: {name}')
            if GETXIAZAI(url, os.path.join(folder_name, name), progress_bar, progress_text):
                st.write(f'下载成功: {name}')
            else:
                st.write(f'下载失败: {name}')
        except Exception as e:
            st.write(f'下载失败: {name}，错误: {e}')
        progress_bar.progress((index + 1) / total_songs)

# 获取歌曲的最终下载链接
def get_redirect_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    response = requests.get(url, headers=headers)
    url_true = response.url
    return url_true

# Streamlit 应用
def main():
    st.title("网易云音乐下载器")
    st.write("请输入歌单ID或歌曲ID，例如：2566843552")
    playlist_id = st.text_input("歌单ID", placeholder="请输入歌单ID")
    song_id = st.text_input("歌曲ID", placeholder="请输入歌曲ID")
    if st.button("下载歌单"):
        if playlist_id:
            url = f'https://music.163.com/playlist?id={playlist_id}'
            lists = getAllMusicList(url)
            if lists:
                downloadMusicList(lists)
            else:
                st.error("未能获取歌单信息，请检查歌单ID是否正确。")
        else:
            st.warning("请输入歌单ID！")
    elif st.button("下载单首歌曲"):
        if song_id:
            url = f'http://music.163.com/song/media/outer/url?id={song_id}.mp3'
            redirect_url = get_redirect_url(url)
            if redirect_url:
                progress_bar = st.progress(0)
                progress_text = st.empty()
                GETXIAZAI(redirect_url, f"歌曲_{song_id}", progress_bar, progress_text)
            else:
                st.error("未能获取歌曲的下载链接，请检查歌曲ID是否正确。")
        else:
            st.warning("请输入歌曲ID！")

if __name__ == "__main__":
    main()