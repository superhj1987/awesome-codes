#!/bin/bash

sed  1"i\allow $1;" /usr/local/nginx/conf/deny.conf > /usr/local/nginx/conf/deny.conf.tmp;
cat /usr/local/nginx/conf/deny.conf.tmp > /usr/local/nginx/conf/deny.conf;
d=`date +"[%Y-%m-%d-%T]"`;
echo "/etc/init.d/nginx reload" > /usr/local/nginx/conf/nginx_reload.txt;
