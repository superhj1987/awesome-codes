--限流lua脚本，推荐使用Nginx自带的ngx_http_limit_conn_module和ngx_http_limit_req_module

-- lua_shared_dict url_limit 1m; //共享全局变量，在所有worker间共享。需要在nginx.conf中配置。在location中通过access_by_lua_file "nginx-limit.lua"使用此脚本。

ngx.header.content_type = "text/html; charset=utf-8";
local method=ngx.req.get_method()
local curl=ngx.md5(ngx.var.request_uri);
local request_uri_without_args = ngx.re.sub(ngx.var.request_uri, "\\?.*", "");
local match = string.match
local ngxmatch=ngx.re.match

--限流计数
local function limit_url_check(key,s,m)
    local localkey=key
    local yyy_limit=ngx.shared.url_limit
    local key_m_limit=localkey..os.date("%Y-%m-%d %H:%M", ngx.time())
    local key_s_limit=localkey..os.date("%Y-%m-%d %H:%M:%S", ngx.time())
    local req_key,_=yyy_limit:get(localkey);
    local req_key_s,_=yyy_limit:get(key_s_limit);
    local req_key_m,_=yyy_limit:get(key_m_limit);

    if req_key_s then
        yyy_limit:incr(key_s_limit,1)
        if req_key_s>s then
            return true
        end
    else
        yyy_limit:set(key_s_limit,1,60)
    end

--    if req_key_m then
--        yyy_limit:incr(key_m_limit,1)
  --      if req_key_m>m then
    --        return true
      --  end
    --else
    --    yyy_limit:set(key_m_limit,1,85)
  --  end

    return false
end

if ngx.re.match(request_uri_without_args,"/(.*)") then
   local url_args = ngx.req.get_uri_args()
   if limit_url_check(curl,100,32000) then --这里是限制某个接口的访问频率，如果写死那么则是整个服务限流，如果是ip根据ip限流
        ngx.exit(ngx.HTTP_FORBIDDEN)
        return
    end
end

return
