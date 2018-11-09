var wy = 0;
var qq = 1;
var kg = 2;
var current = 1;//当前页数
var limit = 20;//分页数量
var musicLength = 0;//歌单长度
var ap;//播放器
var musicList = new Array();//歌单
var song  = new Object();//单个歌曲

function aplayerLoadingSong(musicList,type){
    if (ap==null){
        ap = new APlayer({
            container: document.getElementById('aplayer'),
            theme: '#e9e9e9',
            listFolded: true,
            lrcType:3,
            mutex:true,
            audio:musicList
        });
    }
}
var cur_playing_music_id = "0"

function stopPlay(){
    music = document.getElementById(cur_playing_music_id);
    if (music){
        music.pause();
    }
}
function playThis(id){
    if (id==cur_playing_music_id){
        ;
    }
    else{
        stopPlay();
        music = document.getElementById(id);
        if (music){
            music.load()
            cur_playing_music_id = id;
            console.log("cur_playing_music_id:"+cur_playing_music_id)
            music.play();
        }
        else{
            console.log(id,"音乐不存在");
        }
    }
}