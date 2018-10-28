//判断用户名和密码
<? php
   require 'config.php';
   $_pass=sha1($_POST['pass']);
   $query=mysql_query("SELECT user FROM musicplayer_user WHERE
     user='{$_POST['user']}' AND pass='{$_pass}'") or die("SQL 错误！’)；
   if(!mysql_fetch_array( $ query,MYSQL_ASSOC)){
       echo 1;
   }
   mysql_close();
   ?>
   