--可以执行dos命令，但是返回的是系统状态码，默认输出
os.execute()

--io.popen()也可以执行dos命令，但是返回一个文件
local t = io.popen('svn help')
local a = t:read("*all")

--a返回一个字符串，内容是svn help的内容
--如果想执行某命令或程序可选os.execute(),如果还想捕捉该执行结果可用io.popen() eg：复制文件

os.execute("copy" .. originalPath .. "," .. backupPath)
