import time

# 获取封面
import cv2

dickQie = 4


def videoFm(url):
    vidcap = cv2.VideoCapture(url)
    success,image = vidcap.read()
    video_name = url.split('/')
    video_url = url.split('/')
    del video_url[-1]
    video_url = '/'.join(video_url)

    video_name = video_name[-1].split('.')
    del video_name[-1]
    video_name = '.'.join(video_name)
    n=1
    while n < 30:
        success, image = vidcap.read()
        n+=1
    if not os.path.exists(video_url+'/$cover.Img'):
        os.makedirs(video_url+'/$cover.Img')
    # print(video_url + '/$cover.Img/cover_'+ video_name + '.jpg')
    imag = cv2.imwrite(video_url + '/$cover.Img/cover_'+ video_name + '.jpg',image)
    if imag ==True:
        return 'ok'
    else:
        return 'no'

# 读取文件夹的内容(文件目录, mode等于2就只读文件夹、mode等于3就只读视频, timeSprted时间排序选择)
import os
def Read_Dir(route, mode = 1, timeSprted = '0'):
    dir_list = os.listdir(route)
    if timeSprted == '1':
        # 最新日期文件在前面
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(route, x)), reverse=True)
    elif timeSprted == '2':
        # 最新日期文件在后面
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(route, x)))
    NewDir_List = {
        'dir':[],
        'file':[]
    }
    for i in dir_list:
        # print(i[0])
        if i[0] == '$':
            pass
        else:
            if os.path.isdir(os.path.join(route,i)):
                NewDir_List['dir'].append(
                    {
                        'data':i,
                        'cover':'/static/icon/DirIco.png',

                        'time':''
                    }
                )
            elif not os.path.isdir(os.path.join(route,i)) and (mode == 1 or mode == 3):
                file_w = i.split('.')[-1]
                file_name = i.split('.')
                videoZm = ''
                # print(file_name)
                del file_name[-1]
                file_name = '.'.join(file_name)
                if file_w == 'mp4' or file_w == 'avi' or file_w == 'mkv' and (mode == 1 or mode == 3):
                    FileType = 'Video'
                    if os.path.exists(route+'/$cover.Img/cover_'+file_name+'.jpg'):
                        cover = route+'/$cover.Img/cover_'+file_name+'.jpg'
                    else:
                        videoFm(route+'/'+i)
                        cover = route+'/$cover.Img/cover_'+file_name+'.jpg'
                    cover = '/'.join(cover.split('/')[dickQie:])
                    if os.path.exists(route+'/$videozm.File/zm_'+file_name+'.vtt'):
                        videoZm = route+'/$videozm.File/zm_'+file_name+'.vtt'
                    videoZm = '/'.join(videoZm.split('/')[dickQie:])
                    if mode == 3:
                        dic = {
                            'data': i,
                            'cover': cover,
                            'time': '',
                            'FileType': FileType,
                            'videoZm': videoZm
                        }
                        NewDir_List['file'].append(dic)

                elif file_w == 'docx' and mode == 1:
                    cover = '$cover.Img/'
                    FileType = 'file'
                elif file_w == 'jpg' or file_w == 'png' or file_w == 'jpeg' and mode == 1:
                    cover = route + '/' + i if route[-1] != '/' else route + i
                    cover = '/'.join(cover.split('/')[dickQie:])
                    FileType = 'img'
                elif mode == 1:
                    cover = '/static/icon/fileico.png'
                    FileType = 'file'
                if mode == 1:
                    dic = {
                        'data': i,
                        'cover': cover,
                        'time':'',
                        'FileType':FileType,
                        'videoZm':videoZm
                    }
                    NewDir_List['file'].append(dic)
    return NewDir_List

# 获取文件夹封面

# 检测硬盘大小
from psutil import disk_usage
def Get_Disk(route):
    total = disk_usage(route).total/1024/1024/1024
    used = disk_usage(route).used/1024/1024/1024
    free = disk_usage(route).free/1024/1024/1024
    return total, used, free

def check_file(name,i=1,name_top=None):
    if name_top:
        # print(name_top)
        file_n = name_top[0]
        file_w = name_top[1]
    else:
        file_name = name.split('.')
        file_w = file_name[-1]
        del file_name[-1]
        file_n = '.'.join(file_name)
    if os.path.exists(name):
        file_name = file_n+'({})'.format(i) + '.' + file_w
        return check_file(file_name,i+1,[file_n,file_w])
    else:
        return name

# 字节转换
def byte_to_kb_mb(b):
    b = int(b)
    if b >= 1024:
        kb = b / 1024
        if kb >=1024:
            mb = kb / 1024
            if mb >= 1024:
                gb = mb / 1024
                gb = format(gb, '.1f')
                return str(gb) + 'GB'
            mb = format(mb, '.1f')
            return str(mb) + 'MB'
        else:
            kb = format(kb, '.1f')

            return str(kb)+ 'KB'
    else:
        return str(b) + 'bis'

# 删除文件夹下所有文件
def deleteDir(path):
    if os.path.isdir(path):
        for i in os.listdir(path):
            if os.path.isdir(path + '/' + i):
                deleteDir(path + '/' + i)
                os.rmdir(path + '/' + i)
            else:
                os.remove(path + '/' + i)


def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0

    if not os.path.exists(fileOrFolderPath):
        return totalSize

    if os.path.isfile(fileOrFolderPath):
        totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
        return totalSize

    if os.path.isdir(fileOrFolderPath):
        with os.scandir(fileOrFolderPath) as dirEntryList:
            for curSubEntry in dirEntryList:
                curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                if curSubEntry.is_dir():
                    curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                    totalSize += curSubFolderSize
                elif curSubEntry.is_file():
                    curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                    totalSize += curSubFileSize

            return totalSize


# oss
import oss2
def ReadOss_Dir(bucket, route, mode = 1):
    dir_list = oss2.ObjectIterator(bucket, prefix=route, delimiter='/')
    NewDir_List = {
        'dir':[],
        'file':[]
    }
    for i in dir_list:
        # print(i[0])
        if i.is_prefix():
            dirName = (i.key).split('/')[-2]
            NewDir_List['dir'].append(
                {
                    'path':i.key,
                    'cover':'/static/icon/DirIco.png',
                    'time':'',
                    'data':dirName
                }
            )
        elif not i.is_prefix() and mode == 1:
            if i.key == route:
                continue
            file_w = (i.key).split('.')[-1]
            file_name = (i.key).split('.')
            # print(file_name)
            del file_name[-1]
            file_name = '.'.join(file_name)
            if file_w == 'mp4' or file_w == 'avi' or file_w == 'mkv':
                FileType = 'Video'
                cover = '/static/icon/fileico.png'
                # if os.path.exists(route+'/$cover.Img/cover_'+file_name+'.jpg'):
                #     cover = route+'/$cover.Img/cover_'+file_name+'.jpg'
                #
                # else:
                #     videoFm(route+'/'+i)
                #     cover = route + '/$cover.Img/cover_' + i+'.jpg'
                # cover = '/'.join(cover.split('/')[3:])

            elif file_w == 'docx':
                cover = '$cover.Img/'
                FileType = 'file'
            elif file_w == 'jpg' or file_w == 'png' or file_w == 'jpeg':
                # cover = route + '/' + i if route[-1] != '/' else route + i
                # cover = '/'.join(cover.split('/')[dickQie:])
                cover = '/' + i.key
                FileType = 'img'
            else:
                cover = '/static/icon/fileico.png'
                FileType = 'file'
            fileName = (i.key).split('/')[-1]
            dic = {
                'path': i.key,
                'data': fileName,
                'cover': cover,
                'time':'',
                'FileType':FileType

            }
            NewDir_List['file'].append(dic)
    return NewDir_List




# 721881156
# print(byte_to_kb_mb(763775044))
# print(Read_Dir('C:/Users/yao/Desktop/dir_test'))
# a,b,c = zd('E:\\')
# print(a,b,c)