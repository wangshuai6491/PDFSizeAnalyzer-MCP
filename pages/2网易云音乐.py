import requests
import re
import os
import time

# 下载单首歌曲代码
def GETXIAZAI(url):
    houzhui = url[-4:]
    res = requests.get(url)
    data = res.content
    with open('歌曲' + houzhui, 'wb') as f:
        f.write(data)

def get_redirect_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'}
    response = requests.get(url, headers=headers)
    url_true = response.url
    return url_true

# 下载歌单所用代码
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
    ticks = time.strftime("%Y-%m-%d %H%M%S", time.localtime())
    cur_path = os.path.abspath(os.curdir)
    folder_name = 'music' + str(ticks)
    os.mkdir(os.path.join(cur_path, folder_name))
    weizhi = os.path.join(cur_path, folder_name)

    for i in lists:
        url = i[1]
        name = i[0]
        try:
            print('正在下载', name)
            houzhui = url[-4:]
            r = requests.get(url)
            with open(os.path.join(weizhi, name + houzhui), 'wb') as f:
                f.write(r.content)
            print('下载成功')
        except:
            print('下载失败')

def main(url):
    lists = getAllMusicList(url)
    downloadMusicList(lists)

if __name__ == "__main__":
    print('本程序将下载网易云音乐歌单的歌曲')
    print('需要输入歌曲ID，比如https://music.163.com/playlist?id=2566843552,歌单ID就是2566843552')
    id = input('请输入歌单ID：')
    url = f'https://music.163.com/playlist?id={id}'
    main(url)