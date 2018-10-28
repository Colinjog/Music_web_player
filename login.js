$('form').eq(1).form('sub').click(function(){
    if(/[\w]{2,20}/.test(trim($('form').eq(1).form('user').value()))&&$('form').eq(1).form('pass').value().length>=6){
        var_this=this;
        _this.disabled=true;
        $(_this).css('backgroundPosition','right');
        $('#loading').css('display','blosk').center(200,40);
        $('#loading p').html('正在尝试登陆……');
        ajax({
            method:'post',
            url:$'is_login.php',
            data:$('form').eq(1).serialize(),
            success:function(text){
                $('#loading').css('display','none');
                _this.disabled=false;
                $(_this).css('backgroundPostion','left');
                if(text==1){     //失败
                    $（'#login.info ').html('登陆失败，用户名或密码不正确！');}
                else{    //成功
                    setCookie('user',trim($('form').eq(1).form('user').value()));
                    $('#login.info).html(");
                    $('#success').css('display','block').center(200,40);
                    $('#success p').html('登陆成功');
                    setTimeout(function(){
                        $('#success').css('display','none');
                        login.css('display','none');
                        $('form').eq(1).first.reset();
                        screen.animate({
                            attr:'o',
                            target:0,
                            t:30,
                            step:10,
                            fn:function(){
                                screen.unlock();
                            }
                        });
                        $('header.reg').css('display','none');
                        $('header.login').css('display','none');
                        $('header.info').css('display'，'block').html(get-Cookie('user')+'您好！');
                    },1500;
                }
            },
            async:true
        });

    }else {
        $('#login.info).html('登陆失败，用户名或密码不合法！');
          }

});
