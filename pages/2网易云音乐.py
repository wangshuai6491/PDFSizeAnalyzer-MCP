import re
import io
import zipfile
import requests
import streamlit as st

# ---------- 工具 ----------
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def suffix(content_type: str) -> str:
    if "audio/mpeg" in content_type:
        return ".mp3"
    if "audio/flac" in content_type:
        return ".flac"
    if "audio/wav" in content_type:
        return ".wav"
    return ".mp3"

def sanitize(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", name)

# ---------- 单首 ----------
def fetch_song(song_id: str) -> tuple[str, bytes]:
    url = f"http://music.163.com/song/media/outer/url?id={song_id}"
    resp = requests.head(url, headers=UA, allow_redirects=True)
    if resp.status_code != 200:
        raise RuntimeError(f"无法获取歌曲：{resp.status_code}")
    final_url = resp.url
    suffix_name = suffix(resp.headers.get("content-type", ""))
    music_bytes = requests.get(final_url, headers=UA).content
    return f"{sanitize(song_id)}{suffix_name}", music_bytes

# ---------- 歌单 ----------
def parse_playlist_html(playlist_id: str):
    url = f"https://music.163.com/playlist?id={playlist_id}"
    html = requests.get(url, headers=UA).text
    pattern = re.compile(r'<a href="/song\?id=(\d+)">([^<]+)</a>')
    return [(sid, sanitize(name)) for sid, name in pattern.findall(html)]

def fetch_playlist(playlist_id: str) -> tuple[str, bytes]:
    songs = parse_playlist_html(playlist_id)
    if not songs:
        raise RuntimeError("歌单解析失败或为空")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for sid, name in songs:
            try:
                file_name, data = fetch_song(sid)
                zf.writestr(f"{name}{suffix('audio/mpeg')}", data)
            except Exception:
                continue  # 跳过失效/无版权
    zip_buffer.seek(0)
    return f"{playlist_id}.zip", zip_buffer.getvalue()

# ---------- Streamlit ----------
def main():
    st.set_page_config("网易云音乐下载器", "🎵")
    st.markdown("### 网易云音乐下载")
    # 歌曲或歌单id获取方法
    st.caption("支持单首歌曲和整歌单下载，仅供学习和研究使用，请在 24 小时内删除下载的文件")
    st.caption("歌曲ID获取方法：从歌曲页面URL中获取，如 https://music.163.com/song?id=2716119292 中的 2716119292")
    st.caption("歌单ID获取方法：从歌单页面URL中获取，如 https://music.163.com/playlist?id=2566843552 中的 2566843552")
    st.divider()

    mode = st.radio("选择模式", ["单首歌曲", "整歌单"], horizontal=True)

    if mode == "单首歌曲":
        sid = st.text_input("歌曲 ID", placeholder="2716119292")
        if st.button("下载", type="primary") and sid:
            with st.spinner("获取中..."):
                fname, data = fetch_song(sid)
            st.download_button("⬇️ 立即下载", data, fname)

    else:
        st.error("程序正在开发，暂不支持整歌单下载")
        """
        pid = st.text_input("歌单 ID", placeholder="2566843552")
        if st.button("下载", type="primary") and pid:
            with st.spinner("解析并打包中..."):
                fname, data = fetch_playlist(pid)
            st.download_button("⬇️ 立即下载 ZIP", data, fname)
        """
if __name__ == "__main__":
    main()