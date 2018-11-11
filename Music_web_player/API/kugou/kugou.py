# -*- coding: utf-8 -*-
import requests
from Crypto.Cipher import AES
import base64
from urllib import parse
import json
import html


def getKugouMusic(music, total_count=30):
    music_list = [music+"kugou"]
    songName = {'w':music}
    keyword = parse.urlencode(songName)
    url = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash='
    searchSongUrl = 'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword='+keyword+'&page=1&pagesize='+str(total_count)+'&showtype=1'
    response = requests.get(searchSongUrl)
    response.encoding = response.content
    responseJson = json.loads(response.text)
    '''
            music list
            music_title music_pic_src music_src author time album_pic_src music_id
        '''

    for singleSong in responseJson['data']['info']:
        id = 1000
        music = {}
        s_hash = singleSong['hash']
        s_detailUrl = url+s_hash  # 根据歌的信息获取歌的hash值
        s_response = requests.get(s_detailUrl)
        s_detail = json.loads(s_response.text)  # 详细信息
        s_url = s_detail['data']['play_url']  # 播放url
        s_name = singleSong['songname']  # 歌名
        singer = singleSong['singername']  # 歌手
        s_img = s_detail['data']['img']
        music['music_title'] = s_name
        music['author'] = singer
        music['music_src'] = s_url
        music['music_pic_src'] = s_img
        music['album_pic_src'] = s_img
        music['music_id'] = "{}".format(id)
        id += 1
        music_list.append(music)
        # print(music)
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
    print(getKugouMusic("成都"))
