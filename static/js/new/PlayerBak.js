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
            music.load();
            music.play();
        }
        else{
            console.log(id,"音乐不存在");
        }
    }
}