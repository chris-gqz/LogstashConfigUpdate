# coding=utf-8

# 从日志文件下获取日志名称
def getFileNamesByLogFile(logFilePath):
    # 将路径下的文件名倒入到字典中
    fileNamesDict={}

    for _, _, fileNames in os.walk(logFilePath):
        for fileName in fileNames:
            # value 怎么设置bool  暂定为1
            fileNamesDict[fileName.split(".")[0]]="1"

    return fileNamesDict

# 从配置文件获取索引名称
def getIndexNamesByConfig(configFilePath):
    fileInfo = open(configFilePath)
    indexNamesDict = {}

    for line in fileInfo:
        if "type =>" in line:
            indexNamesDict[line.split('"')[1]] = "1"

    return  indexNamesDict

# 更新配置文件
def updateConfig(ConfigFilePath, LogFilePath, FileNamesDict):
    fileInfo = open(ConfigFilePath,"w")
    fileInfo.truncate()

    input = ""
    output = ""

    for FileName in FileNamesDict:
        inputStr = "input { \n file { \n path => [\""+LogFilePath+"/"+FileName+".*"+"\"] \n type => \""+FileName+"\" \n}\n}\n"
        input += inputStr

        outputStr = "if [type] == \""+FileName+"\" { \n elasticsearch{ \n hosts => [\"http://localhost:9200\"] \n index => \""+FileName.lower()+"\"\n}\n}\n"
        output += outputStr

    fileInfo.write(input)

    fileInfo.write("output {\n")
    fileInfo.write(output)
    fileInfo.write("}\n")

    return



# 判断索引名称是否都包含文件名称，不包含则更新配置文件
def UpDateConfigIfNeed(logFilePath,fileNamesDict,configFilePath,indexNamesDict):
    for fileName in fileNamesDict:
        if not indexNamesDict.has_key(fileName):
            print("需要更新！")
            updateConfig(configFilePath, logFilePath, fileNamesDict)
            break
        print("无需更新")

import os

# 日志文件位置
LogFilePath='/Users/rylink/ELK/log'
FileNamesDict=getFileNamesByLogFile(LogFilePath)

# 配置文件位置
ConfigFilePath='/Users/rylink/ELK/logstash-7.9.3/logstashUpdate.conf'
IndexNamesDict=getIndexNamesByConfig(ConfigFilePath)

UpDateConfigIfNeed(LogFilePath,FileNamesDict,ConfigFilePath,IndexNamesDict)








