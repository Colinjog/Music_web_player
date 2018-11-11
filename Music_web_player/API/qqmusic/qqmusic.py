# -*- coding: utf-8 -*-
import requests
from Crypto.Cipher import AES
import base64
from urllib import parse
import json
import html

def getQQMusic(music, total_count=30):
    songName = {'w':music}
    keyword = parse.urlencode(songName)
    music_list = [music+"qq"]
    # print('-----------QQ音乐-------------')
    headers = {
        'Accept': 'text / javascript, application / javascript, application / ecmascript, application / x - ecmascript, * / *; q = 0.01',
        'Referer': 'https: // y.qq.com / portal / search.html',
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 65.0.3325.181 Safari / 537.36 X - Requested - With: XMLHttpRequest',
    }
    response = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=58435353679204003&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&'+keyword+'&g_tk=5381&jsonpCallback=MusicJsonCallback5675393515972262&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0')
    response.encoding = response.content
    responseJson = response.text[response.text.index('(')+1: -1]
    s_info = json.loads(responseJson)['data']['song']['list']
    count = 1
    temp = 2000
    for name in s_info:
        if count > total_count:
            break

        s_name = name['title']  # 歌名
        s_singer = name['singer'][0]['name']  # 歌手
        s_fileid = name['file']['media_mid']
        s_mid = name['mid']  # QQ音乐的歌曲url要先获得两个mid再将url拼接起来
        s_pic_mid = name['album']['mid']
        s_img = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000{0}.jpg?max_age=2592000'.format(s_pic_mid)  # 封面
        new_url = r'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback8306739466623028&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback8306739466623028&uin=0&songmid='+s_mid+'&filename=C400'+s_fileid+'.m4a&guid=4698951200'
        song_response = requests.get(new_url)
        song_response_text = song_response.text[song_response.text.index('(')+1: -1]
        # print(song_response_text)
        single_s_info = json.loads(song_response_text)['data']['items'][0]
        s_filename = single_s_info['filename']
        vKey = single_s_info['vkey']  # 获取mid后在新的url中得到vkey拼接最终的url
        song_url = 'http://dl.stream.qqmusic.qq.com/'+s_filename+'?vkey='+vKey+'&guid=4698951200&uin=0&fromtag=66'  # 播放url
        if vKey != '':
            # print(song_url + '\n' + s_name, s_singer, s_img)
            count += 1
        '''
                    music list
                    music_title music_pic_src music_src author time album_pic_src music_id
         '''
        music = dict()
        music['music_title'] = s_name
        music['music_src'] = song_url
        music['author'] = s_singer
        music['music_pic_src'] = s_img
        music['album_pic_src'] = s_img
        music['music_id'] = "{}".format(temp)

        temp += 1
        music_list.append(music)
    return music_list
def get_params(s_id):
    first_param = '{{"ids":"[{0}]","br":128000,"csrf_token":""}}'.format(str(s_id))  # json用format时要用两个大括号,否则会抛出keyerror
    # ids:歌曲id
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    forth_param = "0CoJUm6Qyw8W8jud"
    # 三个固定参数
    iv = "0102030405060708"
    first_key = forth_param
    # second_key = 16 * 'F'
    second_key = 'a8LWv2uAtXjzSfkQ'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():  # 用于服务器反解码的key second_param,third_param,second_key不变 该值就不变
    encSecKey = "2d48fd9fb8e58bc9c1f14a7bda1b8e49a3520a67a2300a1f73766caee29f2411c5350bceb15ed196ca963d6a6d0b61f3734f0a0f4a172ad853f16dd06018bc5ca8fb640eaa8decd1cd41f66e166cea7a3023bd63960e656ec97751cfc7ce08d943928e9db9b35400ff3d138bda1ab511a06fbee75585191cabe0e6e63f7350d6"
    return encSecKey


def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    if type(text) is bytes:
        text = str(text, "utf-8")
    text = text + pad * chr(pad)  # 此处aec加密使用16位Bytes text不是16的倍数要补位
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    response = requests.post(url, headers=headers, data=data)
    return response.text




if __name__ == '__main__':
    print(getQQMusic('hello'))

