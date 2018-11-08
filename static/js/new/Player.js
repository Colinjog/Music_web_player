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