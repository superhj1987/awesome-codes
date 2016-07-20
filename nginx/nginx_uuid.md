# 使用nginx_lua即可实现 
set_by_lua $uuid ' local t = io.popen("cat /proc/sys/kernel/random/uuid") return t:read("*all") ';
