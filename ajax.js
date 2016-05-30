function $(p){return document.getElementById(p);}

var http_request=false;
function send_request(url)
{
    //初始化,指定处理函数,发送请求的函数
    http_request=false;
    //开始初始化xmlhttprequest对象
    if(window.XMLHttpRequest)
    {
        //mozilla浏览器
        http_request=new XMLHttpRequest();
        if(http_request.overrideMimeType)
        {
            //设置mime类别
            http_request.overrideMimeType("text/xml");
        }
    }
    else if(window.ActiveXObject)
    {
        //ie浏览器
        try{
            http_request=new ActiveXObject("Msxml2.XMLHTTP");
        }catch(e){
            try{
                http_request=new ActiveXObject("Microsoft.XMLHTTP");
            }catch(e){}
        }
    }
    if(!http_request){//异常,创建对象实体失败
        window.alert("不能创建XMLHttpRequest对象实例");
        return false;
    }
    //确定发送请求的方式和url以及是否同步执行下段代码
    http_request.open("GET",url,true);
    //指定响应处理函数
    http_request.onreadystatechange=processRequest;
    http_request.send("");
}

function processRequest(){
    if(http_request.readyState==4){//判断对象状态
    //alert(http_request.status);
        if(http_request.status==200){//信息已经成功返回,开始处理信息
            //document.all['passport1'].innerHTML =http_request.responseText;
            if(http_request.responseText!="")
                alert(http_request.responseText);
            else
                fnGoHome();
        }else{//页面不能正常显示
            alert("您的请求页面有异常");
        }
    }
}
