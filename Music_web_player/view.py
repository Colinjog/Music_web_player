from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from Music_web_player.API.NetEase.api import NetEase, Parse
def index(request):
    # if request.COOKIES.get('username'):
    print(request.COOKIES)
    context = {}

    context['music_list'] = _search('shake it off')

    return render(request,'MainView/index.html',context)
    # else:
    #     return HttpResponseRedirect(reverse('login:sign_in'))


def default_index(request):
    return render(request,'MainView/index2.html')


def text(request):
    return render(request, 'MainView/test.html')

def search(request):

    if request.method == "POST":
        pass


def _search(music):
    api = NetEase()
    songs = api.search(music)

    '''
        music list
        music_title music_pic_src music_src author time album_pic_src music_id
    '''
    songs = songs['songs']
    music_list = []
    try:

        for song in songs:
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

            temp['album_pic_src'] = api.album(album_id)[0]['al']['picUrl']
            if not 'picUrl' in song.keys():
                temp['music_pic_src'] = temp['album_pic_src']
            else:
                temp['music_pic_src'] = song['picUrl']
            temp['tlyrics'] = api.song_tlyric(temp['music_id'])
            # print(temp)
            music_list.append(temp)
            if len(music_list)>=10:
                break
    except KeyError:
        print("KeyError")
    finally:
        pass
    return music_list

if __name__=="__main__":
    _search("hello")
    _search('shake it off')