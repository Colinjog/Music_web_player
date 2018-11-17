from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from .API.NetEase.api import Parse, NetEase
from django.core.signing import TimestampSigner
from login.models import Account
from Music_web_player.API.kugou.kugou import getKugouMusic
from Music_web_player.API.kuwo.kuwo import getKuwoMusic
from Music_web_player.API.qqmusic.qqmusic import getQQMusic
from django.core.signing import SignatureExpired
MUSIC_LIST = []#index0存储歌曲信息
platform = 'qq'

def index(request):
    username = request.COOKIES.get('username')
    signer = TimestampSigner()
    try:
        username = signer.unsign(username,max_age=7200)
    except SignatureExpired:
        return HttpResponseRedirect('/login/sign_in/')
    except TypeError:
        return HttpResponseRedirect('/login/sign_in/')
    print("username: unsigned ",username)
    if Account.objects.filter(username=username):
        print(request.COOKIES)
        context = {}
        context['username'] = username[:10]
        if len(MUSIC_LIST)<1 or MUSIC_LIST[0]!='成都':
            _search_multi_api("成都",'qq',counts=30)
        context['page'] = 1
        pages = len(MUSIC_LIST)//20 + 1
        pages_list = [x+1 for x in range(pages)]
        context['pages_list'] = pages_list
        try:
            context['music_list'] = MUSIC_LIST[1:21]
        except IndexError:
            context['music_list'] = MUSIC_LIST[1:-1]
        #    20
        # 首歌一页
        page = 1
        context['page'] = 1
        if (page > 1):
            context['prev_page'] = page - 1
        else:
            context['prev_page'] = 1
        if (page < len(MUSIC_LIST) - 1):
            context['next_page'] = page + 1
        else:
            context['next_page'] = len(MUSIC_LIST) - 1
        context['last_page'] = len(MUSIC_LIST)//20+1
        # print(response.content)
        response = render(request, 'MainView/index.html', context)
        response.set_cookie("username",signer.sign(username))
        return response
    else:
        return HttpResponseRedirect(reverse('login:sign_in'))


def default_index(request):
    return render(request,'MainView/index2.html')


def text(request):
    return render(request, 'MainView/test.html')


def search(request,page):
    global platform
    username = request.COOKIES['username']
    print("Platform:",request.POST.get('platform'))
    signer = TimestampSigner()
    try:
        username = signer.unsign(username,max_age=7200)
    except SignatureExpired:
        return HttpResponseRedirect('/login/sign_in/')
    if Account.objects.filter(username=username):
        global MUSIC_LIST

        if (request.POST.get('platform')):
            platform = request.POST.get("platform")
            print("platform:",platform)
        context = {}
        context['username'] = username[:10]
        print('music:',request.POST.get('music'))
        music = request.POST.get('music')

        print(music)
        if not music:
            temp = platform
        else:
            temp = music + platform
        print("length of Music_List:",len(MUSIC_LIST))
        if len(MUSIC_LIST)<1 or ((MUSIC_LIST[0]!=(temp)) and music):#加入平台
            _search_multi_api(music,platform)
        (xindex,yindex) = (20*page-19,1+20*page)
        try:
            context['music_list'] = MUSIC_LIST[xindex:yindex]
        except IndexError:
            context['music_list'] = MUSIC_LIST[xindex:-1]
        print("length:",len(context['music_list']))
        context['page'] = page
        pages = (len(MUSIC_LIST)-2) // 20 + 1
        pages_list = [x + 1 for x in range(pages)]
        context['pages_list'] = pages_list
        if (page>1):
            context['prev_page'] = page-1
        else:
            context['prev_page'] = 1
        if page<((len(MUSIC_LIST)-2)//20+1):
            context['next_page'] = page + 1
        else:
            context['next_page'] = (len(MUSIC_LIST)-2)//20 + 1
        context['last_page'] = (len(MUSIC_LIST)-2)//20 + 1
        return render(request,'MainView/index.html',context)
    else:
        return HttpResponseRedirect(reverse('login:sign_in'))

# def _search(music,counts=30):
#     api = NetEase()
#     songs = api.search(music)
#
#     '''
#         music list
#         music_title music_pic_src music_src author time album_pic_src music_id lyrics
#     '''
#     songs = songs['songs']
#     music_list = []
#
#
#     for song in songs:
#         try:
#             temp = {}
#             temp['music_id'] = song['id']
#             temp['music_title'] = song['name']
#             temp['author'] = song['artists'][0]['name']
#             songs_url = api.songs_url(ids=[temp['music_id']])
#             album_id = song['album']['id']
#             if songs_url:
#                 temp['music_src'] = songs_url[0]['url']
#             else:
#                 temp['music_src'] = ""
#                 #bug
#                 temp['music_src'] = "http://music.163.com/song/media/outer/url?id={}".format(temp['music_id'])
#
#             # temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
#
#             if ('picUrl' in api.album(album_id)[0]['al'].keys()):
#                 temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
#             else:
#                 temp['album_pic_src'] = ""
#             if not 'picUrl' in song.keys():
#                 temp['music_pic_src'] = temp['album_pic_src']
#             else:
#                 temp['music_pic_src'] = song['picUrl']
#             temp['tlyrics'] = api.song_tlyric(temp['music_id'])
#             # temp['time'] = song
#             # print(temp)
#         except KeyError:
#             print("KeyError")
#         except IndexError:
#             if not 'album_pic_src' in temp.keys():
#                 temp['album_pic_src'] = ""
#                 temp['music_pic_src'] = temp['album_pic_src']
#         finally:
#             music_list.append(temp)
#             if len(music_list)>=counts:
#                 break
#     global MUSIC_LIST
#     MUSIC_LIST = [music+"wy"]
#     MUSIC_LIST.extend(music_list)
#     return music_list
#

def _search_multi_api(music,platform, counts=30):
    """

    :string musicname music:
    :wy qq kugou kuwo platform:
    :int counts:
    :return music list:
    """
    global MUSIC_LIST
    if platform=="wy":
        pass
        # _search(music)
    elif platform=="qq":
        music_list = getQQMusic(music,total_count=counts)

        MUSIC_LIST = music_list
        return music_list
    elif platform=="kugou":
        music_list = getKugouMusic(music,total_count=counts)

        MUSIC_LIST = music_list
        return music_list
    elif platform=="kuwo":
        music_list = getKuwoMusic(music,total_count=counts)

        MUSIC_LIST = music_list
        return music_list
    else:
        print("音乐平台不存在")

# def playlist():
#     api = NetEase()
#     songs = api.top_playlists()
#     music_list = []
#     for song in songs:
#         try:
#             temp = {}
#             temp['music_id'] = song['id']
#             temp['music_title'] = song['name']
#             temp['author'] = song['artists'][0]['name']
#             songs_url = api.songs_url(ids=[temp['music_id']])
#             album_id = song['album']['id']
#             if songs_url:
#                 temp['music_src'] = songs_url[0]['url']
#             else:
#                 temp['music_src'] = ""
#                 #bug
#                 temp['music_src'] = "http://music.163.com/song/media/outer/url?id={}".format(temp['music_id'])
#
#             # temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
#
#             if ('picUrl' in api.album(album_id)[0]['al'].keys()):
#                 temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
#             else:
#                 temp['album_pic_src'] = ""
#             if not 'picUrl' in song.keys():
#                 temp['music_pic_src'] = temp['album_pic_src']
#             else:
#                 temp['music_pic_src'] = song['picUrl']
#             temp['tlyrics'] = api.song_tlyric(temp['music_id'])
#             # temp['time'] = song
#             # print(temp)
#         except KeyError:
#             print("KeyError")
#         except IndexError:
#             if not 'album_pic_src' in temp.keys():
#                 temp['album_pic_src'] = ""
#                 temp['music_pic_src'] = temp['album_pic_src']
#         finally:
#             music_list.append(temp)
#             if len(music_list)>=100:
#                 break
#     global MUSIC_LIST
#     MUSIC_LIST = ['index']
#     MUSIC_LIST.extend(music_list)
#     return music_list
if __name__=="__main__":
    # _search("hello")
    # _search('shake it off')
    # print(_search("hello"))
    # print(_search("成都"))
    pass