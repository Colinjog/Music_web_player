# -*- coding: utf-8 -*-
import requests
from Crypto.Cipher import AES
import base64
from urllib import parse
import json
import html





def getKuwoMusic(music, total_count=30):
    songName = {'w':music}
    keyword = parse.urlencode(songName)
    music_list = [music+"kuwo"]
    baseurl = 'http://search.kuwo.cn/r.s?all={0}&ft=music&itemset=web_2013&client=kt&pn=0&rn={1}&rformat=json&encoding=utf8'.format(keyword, str(total_count))
    kuwo_picurl = 'http://www.kuwo.cn/webmusic/sj/dtflagdate?flag=6&rid={0}'
    song_list_response = requests.get(baseurl)
    song_list_response.encoding = song_list_response.content
    song_list_json = json.loads(song_list_response.text.replace("'", '"'))['abslist']  # 不能用单引号括起字符串
    for song in song_list_json:
        # print(song)
        s_name = html.unescape(song['SONGNAME'])  # 歌名
        singer = html.unescape(song['ARTIST'])  # 歌手
        s_id = song['MUSICRID']
        s_url = 'http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=acc|mp3&response=url'.format(s_id)
        s_response = requests.get(s_url)
        s_play_url = s_response.text
        s_img = requests.get(kuwo_picurl.format(s_id)).text.split(',')[1]
        if s_img is None:
            s_img = 'http://image.kuwo.cn/www/default/240-240-person.jpg'
        '''
                    music list
                    music_title music_pic_src music_src author time album_pic_src music_id lyrics
                '''
        music = {}
        music['music_title'] = s_name
        music['music_id'] = s_id
        music['music_src'] = s_play_url
        music['music_pic_src'] = s_img
        music['album_pic_src'] = s_img
        music['author'] = singer
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
    print(getKuwoMusic("hello"))