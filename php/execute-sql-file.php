<?php
/**
* 读取 sql 文件并写入数据库 
* @version 1.01 demo.php 2008/08/21
* @author xingshaocheng <xingshaocheng@foxmail.com>
*/
class DBManager
{
    var $dbHost = '';
    var $dbUser = '';
    var $dbPassword = '';
    var $dbSchema = '';
    
    function __construct($host,$user,$password,$schema)
    {
        $this->dbHost = $host;
        $this->dbUser = $user;
        $this->dbPassword = $password;
        $this->dbSchema = $schema;
    }
    
    function createFromFile($sqlPath,$delimiter = '(;\n)|((;\r\n))|(;\r)',$prefix = '',$commenter = array('#','--'))
    {
        //判断文件是否存在
        if(!file_exists($sqlPath))
            return false;
        
        $handle = fopen($sqlPath,'rb');    
        
        $sqlStr = fread($handle,filesize($sqlPath));
        
        //通过sql语法的语句分割符进行分割
        $segment = explode(";",trim($sqlStr)); 
        
        //var_dump($segment);
        
        //去掉注释和多余的空行
        foreach($segment as & $statement)
        {
            $sentence = explode("\n",$statement);
            
            $newStatement = array();
            
            foreach($sentence as $subSentence)
            {
                if('' != trim($subSentence))
                {
                    //判断是会否是注释
                    $isComment = false;
                    foreach($commenter as $comer)
                    {
                        if(eregi("^(".$comer.")",trim($subSentence)))
                        {
                            $isComment = true;
                            break;
                        }
                    }
                    //如果不是注释，则认为是sql语句
                    if(!$isComment)
                        $newStatement[] = $subSentence;                    
                }
            }
            
            $statement = $newStatement;
        }
        //对表名加前缀
        if('' != $prefix)
        {
            
        
            //只有表名在第一行出现时才有效 例如 CREATE TABLE talbeName
    
            $regxTable = "^[\`\'\"]{0,1}[\_a-zA-Z]+[\_a-zA-Z0-9]*[\`\'\"]{0,1}$";//处理表名的正则表达式
            $regxLeftWall = "^[\`\'\"]{1}";
            
            $sqlFlagTree = array(
                    "CREATE" => array(
                            "TABLE" => array(
                                    "$regxTable" => 0
                                )
                        ),
                    "INSERT" => array(
                            "INTO" => array(
                                "$regxTable" => 0
                            )
                        )
                    
                    );
                            
            foreach($segment as & $statement)
            {
                $tokens = split(" ",$statement[0]);
                
                $tableName = array();
                $this->findTableName($sqlFlagTree,$tokens,0,$tableName);
                
                if(empty($tableName['leftWall']))
                {
                    $newTableName = $prefix.$tableName['name'];
                }
                else{
                    $newTableName = $tableName['leftWall'].$prefix.substr($tableName['name'],1);
                }
                
                $statement[0] = str_replace($tableName['name'],$newTableName,$statement[0]);
            }
            
        }        
        //组合sql语句
        foreach($segment as & $statement)
        {
            $newStmt = '';
            foreach($statement as $sentence)
            {
                $newStmt = $newStmt.trim($sentence)."\n";
            }
                
            $statement = $newStmt;
        }
        
        //用于测试------------------------        
        //var_dump($segment);
        //writeArrayToFile('data.txt',$segment);
        //-------------------------------
        
        self::saveByQuery($segment);
        
        return true;
    }
    
    private function saveByQuery($sqlArray)
    {
        $conn = mysql_connect($this->dbHost,$this->dbUser,$this->dbPassword);
        
        mysql_select_db($this->dbSchema);
        
        foreach($sqlArray as $sql)
        {
            mysql_query($sql);
        }        
        mysql_close($conn);
    }
    
    private function findTableName($sqlFlagTree,$tokens,$tokensKey=0,& $tableName = array())
    {
        $regxLeftWall = "^[\`\'\"]{1}";
        
        if(count($tokens)<=$tokensKey)
            return false;        
        
        if('' == trim($tokens[$tokensKey]))
        {
            return self::findTableName($sqlFlagTree,$tokens,$tokensKey+1,$tableName);
        }
        else
        {
            foreach($sqlFlagTree as $flag => $v)
            {    
                if(eregi($flag,$tokens[$tokensKey]))
                {
                    if(0==$v)
                    {
                        $tableName['name'] = $tokens[$tokensKey];
            
                        if(eregi($regxLeftWall,$tableName['name']))
                        {
                            $tableName['leftWall'] = $tableName['name']{0};
                        }
                        
                        return true;
                    }
                    else{
                        return self::findTableName($v,$tokens,$tokensKey+1,& $tableName);
                    }
                }
            }
        }
        
        return false;
    }
}

function writeArrayToFile($fileName,$dataArray,$delimiter="\r\n")
{
    $handle=fopen($fileName, "wb");
    
    $text = '';
    
    foreach($dataArray as $data)
    {
        $text = $text.$data.$delimiter;
    }
    fwrite($handle,$text);
}

//测试
$dbM = new DBManager('localhost','w01f','123456','test');
$dbM->createFromFile('data.sql',null,'fff_');
?>

data.sql:

-- phpMyAdmin SQL Dump
-- version 2.11.3
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2008 年 08 月 20 日 12:09
-- 服务器版本: 5.0.51
-- PHP 版本: 5.2.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- 数据库: `newysh`
--

-- --------------------------------------------------------

--
-- 表的结构 `allowed`
--

CREATE TABLE `allowed` (
`bhash` blob NOT NULL,
`bname` varchar(255) character set utf8 NOT NULL,
PRIMARY KEY (`bhash`(20))
) ENGINE=MyISAM DEFAULT CHARSET=gb2312 ROW_FORMAT=DYNAMIC;

--
-- 导出表中的数据 `allowed`
--


-- --------------------------------------------------------

--
-- 表的结构 `allowed_ex`
--

CREATE TABLE `allowed_ex` (
`bhash` blob NOT NULL,
`badded` datetime NOT NULL,
`bsize` bigint(20) unsigned NOT NULL,
`bfiles` int(10) unsigned NOT NULL,
PRIMARY KEY (`bhash`(20))
) ENGINE=MyISAM DEFAULT CHARSET=gb2312 ROW_FORMAT=DYNAMIC;

--
-- 导出表中的数据 `allowed_ex`
--


-- --------------------------------------------------------

--
-- 表的结构 `category`
--

CREATE TABLE `category` (
`cid` int(10) unsigned NOT NULL auto_increment COMMENT '种子分类id',
`name` varchar(255) NOT NULL COMMENT '分类名称,支持html格式',
`sequence` int(10) unsigned NOT NULL COMMENT '显示排序，需要小的排在前面',
PRIMARY KEY (`cid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=26 ;

--
-- 导出表中的数据 `category`
--

INSERT INTO `category` (`cid`, `name`, `sequence`) VALUES
(25, '音乐', 23),
(24, '学习资料', 24),
(23, '电影', 25);
