from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Music_web_player.API.NetEase.api import NetEase, Parse


MUSIC_LIST = []#index0存储歌曲信息


def index(request):
    # if request.COOKIES.get('username'):
    print(request.COOKIES)
    context = {}
    if len(MUSIC_LIST)<1 or MUSIC_LIST[0]!='hello':
        _search('hello')
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
    return response
    # else:
    #     return HttpResponseRedirect(reverse('login:sign_in'))


def default_index(request):
    return render(request,'MainView/index2.html')


def text(request):
    return render(request, 'MainView/test.html')


def search(request,page):
    global MUSIC_LIST
    print('music:',request.POST.get('music'))
    music = request.POST.get('music')

    print(music)
    context = {}
    print("length of Music_List:",len(MUSIC_LIST))
    if len(MUSIC_LIST)<1 or (MUSIC_LIST[0]!=music and music):
        _search(music)
    (xindex,yindex) = (20*page-19,1+20*page)
    try:
        context['music_list'] = MUSIC_LIST[xindex:yindex]
    except IndexError:
        context['music_list'] = MUSIC_LIST[xindex:-1]
    print("length:",len(context['music_list']))
    context['page'] = page
    pages = (len(MUSIC_LIST)-1) // 20 + 1
    pages_list = [x + 1 for x in range(pages)]
    context['pages_list'] = pages_list
    if (page>1):
        context['prev_page'] = page-1
    else:
        context['prev_page'] = 1
    if page<((len(MUSIC_LIST)-1)//20+1):
        context['next_page'] = page + 1
    else:
        context['next_page'] = (len(MUSIC_LIST)-1)//20 + 1
    context['last_page'] = (len(MUSIC_LIST)-1)//20 + 1
    return render(request,'MainView/index.html',context)


def _search(music):
    api = NetEase()
    songs = api.search(music)

    '''
        music list
        music_title music_pic_src music_src author time album_pic_src music_id
    '''
    songs = songs['songs']
    music_list = []


    for song in songs:
        try:
            temp = {}
            temp['music_id'] = song['id']
            temp['music_title'] = song['name']
            temp['author'] = song['artists'][0]['name']
            songs_url = api.songs_url(ids=[temp['music_id']])
            album_id = song['album']['id']
            if songs_url:
                temp['music_src'] = songs_url[0]['url']
            else:
                temp['music_src'] = ""
                #bug
                temp['music_src'] = "http://music.163.com/song/media/outer/url?id={}".format(temp['music_id'])

            # temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']

            if ('picUrl' in api.album(album_id)[0]['al'].keys()):
                temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
            else:
                temp['album_pic_src'] = ""
            if not 'picUrl' in song.keys():
                temp['music_pic_src'] = temp['album_pic_src']
            else:
                temp['music_pic_src'] = song['picUrl']
            temp['tlyrics'] = api.song_tlyric(temp['music_id'])
            # temp['time'] = song
            # print(temp)
        except KeyError:
            print("KeyError")
        except IndexError:
            if not 'album_pic_src' in temp.keys():
                temp['album_pic_src'] = ""
                temp['music_pic_src'] = temp['album_pic_src']
        finally:
            music_list.append(temp)
            if len(music_list)>=100:
                break
    global MUSIC_LIST
    MUSIC_LIST = [music]
    MUSIC_LIST.extend(music_list)
    return music_list

if __name__=="__main__":
    # _search("hello")
    # _search('shake it off')
    # print(_search("hello"))
    print(_search("成都"))