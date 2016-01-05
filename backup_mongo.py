#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, time, datetime
import sys,subprocess
from os.path import join

reload(sys)
print '---------------------------------------------------------------------\n'
time1=datetime.datetime.now()#增加统计时长计算，和脚本最后面进行相减操作，计算出脚本执行时长
print '%s   : ........正在进行备份请稍后..........\n'%datetime.datetime.now()
print '%s   : 系统当前默认字符集是： %s\n' % (datetime.datetime.now(), sys.getdefaultencoding())
sys.setdefaultencoding('utf-8')
print '%s   : 修改当前系统字符集为： %s\n' % (datetime.datetime.now(), sys.getdefaultencoding())
# 待导出数据库信息
db_user = 'admin'
db_passwd = 'admin'
db_type = 'mongodb'
mongo_shell_path = '/usr/local/mongodb/bin/mongodump'
mongo_shell_parameter = ' --authenticationDatabase admin'
print '%s   : 待备份数据库类型是： %s\n' % (datetime.datetime.now(), db_type)
#备份文件命名
TARGET_DIR = '/data/backup/'
print '%s   : 备份到本地 %s目录下\n ' % (datetime.datetime.now(), TARGET_DIR)
mongo_file_path = TARGET_DIR+db_type + time.strftime('-%H%M%S')
print '%s   : 数据库导出文件夹是： %s\n' % (datetime.datetime.now(), mongo_file_path)
TARGET =TARGET_DIR+ 'mongoDB-' + time.strftime('%Y%m%d') + '.tar'
print '%s   : 压缩包文件名是： %s\n' % (datetime.datetime.now(), TARGET)
#备份数据库命令
bak_mongo_shell = mongo_shell_path + ' -o ' + mongo_file_path + ' -u ' + db_user + ' -p=' + db_passwd + mongo_shell_parameter
#数据库备份命令原型：/usr/local/mongodb/bin/mongodump -o /data/backup/mongodb-181746 -u admin -p=admin --authenticationDatabase admin
#备份压缩命令
tar_command = 'tar -czf %s %s ' % (TARGET, ''.join(mongo_file_path))
print '%s   : 备份压缩命令是： %s\n' % (datetime.datetime.now(), tar_command)
#执行备份数据库命令
print
#os.system(bak_mongo_shell)
try:#判断mongo导出是否成功
    retcode =subprocess.call(bak_mongo_shell, shell=True)
    if retcode < 0:
        print >>sys.stderr, "mongo导出子进程被终止，返回码是", -retcode
        print '%s   : ........mongo导出备份失败！！..........\n' %datetime.datetime.now()
    if retcode ==0:
        print '%s   : ........mongo导出成功！！..........\n' %datetime.datetime.now()
    else:
        print >>sys.stderr, "mongo导出子进程返回码是", retcode
        print '%s   : ........mongo导出备份失败！！..........\n' %datetime.datetime.now()
except OSError as e:
    print >>sys.stderr, "mongo导出错误信息:", e
    print '%s   : ........mongo导出备份失败！！..........\n' %datetime.datetime.now()
# 判断导出的mongo文件夹大小，来确定是否执行打包命令
def getdirsize(dir):
    size = 0
    for (root, dirs, files) in os.walk(dir):
        for name in files:
            try:
                size += os.path.getsize(join(root, name))
            except:
                continue
    return size

mongo_file_size = getdirsize(mongo_file_path)
# 统计导出的备份文件大小
def format_file(format_file_size):
    size1=format_file_size/(1024.0*1024.0*1024.0)#GB
    size2=format_file_size/(1024.0*1024.0)#MB
    size3=format_file_size/1024.0#KB
    size4=format_file_size#B
    if      size1>1:
        print "%s   : 当前备份的文件大小是： %sGB\n"%(datetime.datetime.now(),round(size1,1))
    elif    size2>1:
        print "%s   : 当前备份的文件大小是： %sMB\n"%(datetime.datetime.now(),round(size2,1))
    elif    size3>1:
        print "%s   : 当前备份的文件大小是： %sKB\n"%(datetime.datetime.now(),round(size3,1))
    else:#这里对文件大小进行判断，当文件大于1M显示的是多少MB，如果当文件小于1M显示的是多少KB，利用round函数进行四舍五入
        print "%s   : 当前备份的文件大小是： %sB\n"%(datetime.datetime.now(),round(size4,3))
if retcode==0 and mongo_file_size==mongo_file_size:#条件1：如果导出mongo备份成功，再执行压缩备份，否则不备份；条件2：如果文件大小相同说明导出到文件已经结束。执行打包命令
    try:
        retcode1 =subprocess.call(tar_command, shell=True)
        if retcode1 < 0:
            print >>sys.stderr, "tar导出子进程被终止，返回码是", -retcode1
            print '%s   : ........tar备份失败！！..........\n' %datetime.datetime.now()
        if retcode1 ==0:
            print '%s   : ........tar备份成功！！..........\n' %datetime.datetime.now()
            tar_file_size=os.path.getsize(TARGET)
            format_file(tar_file_size)
            print '%s   : 备份文件为： %s\n' % (datetime.datetime.now(), TARGET)
        else:
            print >>sys.stderr, "tar导出子进程返回码是", retcode1
            print '%s   : ........tar备份失败！！..........\n' %datetime.datetime.now()
    except OSError as e:
        print >>sys.stderr, "tar导出错误信息:", e
        print '%s   : ........tar备份失败！！..........\n' %datetime.datetime.now()
time2=datetime.datetime.now()
time3=time2-time1
print '此次备份总共耗时:',time3#计算出脚本的执行时长
print '---------------------------------------------------------------------\n'

