# from django.shortcuts import render
from django.shortcuts import render
from django.http import  JsonResponse
from nas.models import *
# Create your views here.
import oss2
import os, shutil, re, datetime
from qbittorrent import Client
from .method import Methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import random
import hashlib

import json
#
# auth = oss2.Auth(' '')
# bucket = oss2.Bucket(auth, '', '')‘
# qbittorrent远程服务端口
qb = Client('http://127.0.0.1:8080/')
# qb.login('admin', '123456')
# 文件保存地址
HomeDisk = ''
# HomeDisk = '/home/diskData1'
# 限速最低速度
minDownloadSpeed = 100
# 限速最高速度
maxDownloadSpeed = 40000
def Md5(str):
  md5 = hashlib.md5()  # 创建md5对象
  # 此处必须声明encode
  # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
  md5.update(str.encode(encoding='utf-8'))
  # 把输入的旧密码装换为md5格式
  result = md5.hexdigest()
  # 返回加密结果
  return result

# 用户账号相关接口
class UserLogin(APIView):
    authentication_classes = []
    def post(self, request):
        # user = request.POST.get('username')
        try:
            UserData = json.loads(request.body)
            userID = UserData['userName']
            userPwd = str(UserData['userPwd'])
            # 密码正则
            pwdRe = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d.#,!]{8,}$'
            userIDRe = '^.*(?=.*[@$%^&*()_+?><:"])[@$%^&*()_+?><:"|/=-]{1,}$'
            if not re.findall(pwdRe, userPwd) or re.findall(userIDRe,userID):
                return JsonResponse({'code': 401, 'msg': '错误'}, status=401)
            userPwd = Md5(userPwd)
            UserData = users_table.objects.filter(user_name=userID, user_pwd=userPwd).first()
            if not UserData:
                # raise exceptions.AuthenticationFailed('403-请登录')
                return JsonResponse({'code': 403, 'msg': '密码错误'}, status=403)

            # 为用户创建token
            zm_list = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','1','2','3']
            mi = random.sample(zm_list, 5)
            token = Md5(str(userID) + userPwd + ''.join(mi))
            # 存在就更新，不存在就创建
            now_time = datetime.datetime.now()
            UserToken.objects.update_or_create(user=UserData, defaults={'token': token, 'time': now_time})

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
            else:
                ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

            UserData.user_last_login = {'time': now_time.strftime('%Y-%m-%d %H:%M:%S'), 'ip': ip}
            UserData.save()
            userDisk = UserData.user_Disk
            if not userDisk:
                userDisk = Md5(userID)
            UserDiskPath = HomeDisk + '/' + userDisk
            if not os.path.exists(UserDiskPath):
                os.makedirs(UserDiskPath)
            UserMsg = {'code': 201, 'msg': '登录成功', 'token': token, 'userName': userDisk,'speed':UserData.user_download_speed}

        except Exception as e:
            UserMsg = {'code': 401, 'msg': '传参出错'}
            return JsonResponse(UserMsg, status=401)

        return JsonResponse(UserMsg)

class UserSign(APIView):
    authentication_classes = []
    def post(self, request):
        UserData = json.loads(request.body)
        userID = UserData['userName']
        userPwd = str(UserData['userPwd'])
        userEmail = UserData['userEmail']
        pwdRe = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d.#,!]{8,}$'
        userIDRe = '^.*(?=.*[@$%^&*()_+?><:"])[@$%^&*()_+?><:"|/=-]{1,}$'

        if (not re.findall(pwdRe, userPwd)) or re.findall(userIDRe, userID):
            return JsonResponse({'code': 401, 'msg': '错误'}, status=401)
        elif users_table.objects.filter(user_name=userID):
            return JsonResponse({'code': 401, 'msg': '用户名已存在'}, status=401)
        elif users_table.objects.filter(user_email=userEmail):
            return JsonResponse({'code': 401, 'msg': '邮箱已存在'}, status=401)
        else:
            userPwd = Md5(userPwd)

            # userNickname = request.POST.get('userNickname')
            # userCover = request.POST.get('userCover')
            # userSex = request.POST.get('userSex')
            #
            # userMobile = request.POST.get('userMobile')
            # userAddress = request.POST.get('userAddress')
            userSignTime = datetime.datetime.now()
            uploadUser = users_table(user_name=userID,
                        user_pwd=userPwd,
                        user_Disk=Md5(userID),
                        user_disk_size=10*1024*1024*1024,
                        user_download_speed=minDownloadSpeed*1024,
                        # user_nickname=userNickname,
                        # user_cover=userCover,
                        # user_sex=userSex,
                        user_email=userEmail,
                        # user_Mobile=userMobile,
                        # user_address=userAddress,
                        user_sign_time=userSignTime)
            uploadUser.save()

            userDisk = Md5(userID)
            UserDiskPath = HomeDisk + '/' + userDisk
            if not os.path.exists(UserDiskPath):
                os.makedirs(UserDiskPath)
            return JsonResponse({'code': 201, 'msg': '注册成功'}, status=201)


class GetUserMsg(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        TokenObj = UserToken.objects.get(token=Usertoken)
        UserMsg = TokenObj.user
        UserDic = {'userName':UserMsg.user_name,
                   'userEmail':UserMsg.user_email,
                   'user_nickname':UserMsg.user_nickname,
                   'user_cover':UserMsg.user_cover}
        return JsonResponse(UserDic)

def checkUser(request):
    if 'Cookie' in request.headers:
        Cookie = request.headers['Cookie']
        UserName = re.findall('UserName=(.*?)as_d\*ax_csd', Cookie)[0] if re.findall('(.*?)as_d\*ax_csd', Cookie) else ''
        Token = re.findall('Token=(.*?);', Cookie)[0] if re.findall('Token=(.*);', Cookie) else None
        if not Token:
            Token = re.findall('Token=(.*)', Cookie)[0] if re.findall('Token=(.*)', Cookie) else ''

        UserSpeed = re.findall('UserSpeed=(.*?)as_d', Cookie)[0] if re.findall('UserSpeed=(.*?)as_d', Cookie) else ''

        # UserName = re.findall('(.*)as_d\*ax_csd', UserName)[0] if re.findall('(.*)as_d\*ax_csd', UserName) else ''
        User = UserToken.objects.get(token=Token).user
        if UserName == User.user_Disk and User.user_download_speed == int(UserSpeed):
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({}, status=404)
    else:
        return JsonResponse({}, status=404)

class UpUserCode(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        TokenObj = UserToken.objects.get(token=Usertoken)
        User = TokenObj.user
        zm_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'n', 'm', 'o', 'p', 'q', 'r', 's', 't',
                   '1', '2', '3', '4', 'ad', 'fv', 'qw', 'hj', 'zz']
        mi = random.sample(zm_list, 5)
        token = Md5(str(User.user_name) + User.user_pwd + ''.join(mi))
        # 存在就更新，不存在就创建
        now_time = datetime.datetime.now()
        UserToken.objects.update_or_create(user=User, defaults={'token': token, 'time': now_time})

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        User.user_last_login = {'time': now_time.strftime('%Y-%m-%d %H:%M:%S'), 'ip': ip}
        User.save()
        UserMsg = {'code': 201, 'msg': '登录成功', 'token': token}
        return JsonResponse({'msg':'更新成功', 'token': token}, status=201)



class GetUsersManage(APIView):
    def get(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if int(UserName.user_lv) != 3:
            return JsonResponse({'msg': '权限不足'})
        UserListDb = users_table.objects.all()
        UserList = [{'id':i.id,
                     'userName':i.user_name,
                     'limitSpeed':'是' if i.user_lv<=1 else '否',
                     'lv': str(i.user_lv)
                     } for i in UserListDb]
        dic = {'UsersList':UserList, 'msg':'获取成功'}
        return JsonResponse(dic)

class DeleteUserManage(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if int(UserName.user_lv) != 3:
            return JsonResponse({'msg': '权限不足'})
        UserData = json.loads(request.body)

        userID = UserData['UserId']
        User = users_table.objects.get(id=userID)
        User.delete()
        return JsonResponse({'msg':'操作成功'})

class UpUserManage(APIView):
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if int(UserName.user_lv) != 3:
            return JsonResponse({'msg': '权限不足'})
        UserData = json.loads(request.body)
        userID = UserData['UserId']
        UserLv = UserData['UserLv']
        UserSeepd = UserData['UserSeepd']

        User = users_table.objects.get(id=userID)

        if int(UserLv)>1:
            DownloadSpeed = 1024 * maxDownloadSpeed
        else:
            DownloadSpeed = 1024 * minDownloadSpeed
        if UserSeepd == '否' and int(UserLv)==User.user_lv and UserLv == '1':
            UserLv = 2

        elif UserSeepd == '是' and int(UserLv)==User.user_lv and UserLv != '1':
            DownloadSpeed = 1024 * minDownloadSpeed
            UserLv = 1

        User.user_lv = UserLv
        User.user_download_speed = DownloadSpeed
        User.save()
        # User.delete()
        return JsonResponse({'msg':'操作成功'})


# def AL_yun(request):
#     directory = []
#     file = []
#     for obj in oss2.ObjectIterator(bucket, prefix='', delimiter='/'):
#         # 通过is_prefix方法判断obj是否为文件夹。
#         if obj.is_prefix():  # 判断obj为文件夹。
#             directory.append(obj.key)
#             # print('directory: ' + obj.key)
#         else:  # 判断obj为文件。
#             file.append(obj.key)
#             # print('file: ' + obj.key)
#
#     # print(dic)
#     return render(request, 'nas/index.html', locals())
#
# def Get_Video(request):
#     url = request.GET.get('url')
#     url = 'https://awowyao.oss-cn-beijing.aliyuncs.com/' + url
#     # print(url)
#     return render(request, 'nas/video.html', locals())


class Read_Dir(APIView):
    def get(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        get_route = request.GET.get('route')
        time_sorted = request.GET.get('timeSorted')
        mode = int(request.GET.get('mode')) if request.GET.get('mode') else 1
        if not time_sorted:
            time_sorted = '0'
        url = HomeDisk + '/' + UserName + get_route
        get_route = Methods.Read_Dir(url, timeSprted=time_sorted,mode=mode)
        return JsonResponse(get_route)


class Read_disk(APIView):
    def get(self, request):
        dirPath = request.GET.get('route')
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        # print(get_route)
        url = HomeDisk + '/' + UserName + dirPath
        get_route = Methods.Read_Dir(url, mode=2)
        # print(get_route)
        dir_list = []
        for i in get_route['dir']:
            dic = {
                'name': i['data'],
                'path': dirPath
            }
            dir_list.append(dic)
        return JsonResponse({'code': 200, 'data': dir_list})

class Get_Disk_Size(APIView):
    def get(self, request):
        token = request.headers
        Usertoken = token['Token']
        User = UserToken.objects.get(token=Usertoken).user
        UserDisk = HomeDisk + '/' + User.user_Disk
        uesSize = Methods.getFileFolderSize(UserDisk)
        dic = {
            'totalSize':  Methods.byte_to_kb_mb(User.user_disk_size),
            'uesSize': Methods.byte_to_kb_mb(uesSize),
            'percentage': format(uesSize / int(User.user_disk_size) * 100, '.1f')
        }
        return JsonResponse(dic)


class Up_Data(APIView):
    @csrf_exempt
    def post(self, request):
        myFile = request.FILES.get("file", None)
        # disk = request.GET.get('route')
        disk = request.POST.get('route')
        token = request.headers
        Usertoken = token['Token']
        User = UserToken.objects.get(token=Usertoken).user
        UserDisk = HomeDisk + '/' + User.user_Disk
        UsertotalSize = User.user_disk_size
        uesSize = Methods.getFileFolderSize(UserDisk)
        diskSize = int(UsertotalSize) - uesSize
        diskSize = diskSize - myFile.size

        if diskSize >= 0:
            disk = '/' + User.user_Disk + '/' + disk
            if not myFile:
                JsonResponse({'msg':'失败'})
            name = Methods.check_file(myFile.name)
            destination = open(os.path.join(HomeDisk + disk , name), 'wb+')  # 打开特定的文件进行二进制的写操作

            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            return JsonResponse({'status':200}, status=201)
        else:
            return JsonResponse({'msg': '空间不足'}, status=403)



class GetFileText(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        if path[0] != '/':
            path = HomeDisk + '/' + UserName + '/' + path
        else:
            path = HomeDisk + '/' + UserName + path
        with open(path, 'r', encoding='utf-8') as f:
            FileText = f.readlines()
            f.close()
        # print(path)
        FileText = ''.join(FileText)
        dic = {'text': FileText,'msg':'获取成功'}
        return JsonResponse(dic, status=200)

class setFileText(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        fileText = PostData['fileText']
        if path[0] != '/':
            path = HomeDisk + '/' + UserName + '/' + path
        else:
            path = HomeDisk + '/' + UserName + path
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fileText)
            f.close()

        dic = {'msg':'保存成功'}
        return JsonResponse(dic, status=200)


class setQbittor(APIView):
    @csrf_exempt
    def post(self, request):
        PostData = (json.loads(request.body))
        torrent = PostData["torrent"]
        path = PostData["path"]
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if UserName.user_lv == 3:
            DownloadDisk = HomeDisk + '/' + UserName.user_Disk + path
            try:
                qb.download_from_link(torrent, savepath=DownloadDisk)
            except:
                qb.login('admin', 'chenwenyao')
                qb.download_from_link(torrent, savepath=DownloadDisk)
            return JsonResponse({'code':200, 'msg':'添加下载成功'})

class getQbDownloadData(APIView):
    def get(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if int(UserName.user_lv) != 3:
            return JsonResponse({'msg':'权限不足'})
        try:
            torrents = qb.torrents()
        except:
            qb.login('admin', 'chenwenyao')
            torrents = qb.torrents()
        torrentsData = []
        for i in torrents:
            qbSize = Methods.byte_to_kb_mb(i['size'])
            qbDownloadCompleted = Methods.byte_to_kb_mb(i['completed'])
            if str(i['size']) == '0':
                ProgressNub = 0
            else:
                ProgressNub = format(i['completed'] / i['size'] * 100, '.1f')
            dlspeed = Methods.byte_to_kb_mb(i['dlspeed']) + '/s'
            # print(dlspeed)
            name = i['name']
            qbstate = i['state']
            if qbstate == 'downloading':
                qbstate = '下载'
            elif qbstate == 'pausedDL':
                qbstate = '暂停'
            elif qbstate == 'stalledDL':
                qbstate = '等待'
            elif qbstate == 'uploading':
                qbstate = '上传'
            elif qbstate == 'pausedUP':
                qbstate = '完成'
            elif qbstate == 'stalledUP':
                qbstate = '做种'
            else:
                qbstate = '未知'
            dic = {
                'name':name,
                'Size':qbSize,
                'Downloadfinish':qbDownloadCompleted,
                'dlspeed':dlspeed,
                'state': qbstate,
                'Progress': ProgressNub,
                'QbHash': i['hash']
            }
            torrentsData.append(dic)
        return JsonResponse({'code': 200, 'QbData': torrentsData})


class ControlQbDownload(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user
        if int(UserName.user_lv) != 3:
            return JsonResponse({'msg': '权限不足'})
        PostData = (json.loads(request.body))
        mode = PostData['mode']
        QbHash = PostData['QbHash']
        if mode == 1:
            qb.resume(QbHash)
        elif mode == 2:
            qb.pause(QbHash)
        elif mode == 3:
            qb.delete(QbHash)
        elif mode == 4:
            qb.delete_permanently(QbHash)
        return JsonResponse({'code':200, 'msg': '修改成功'})


class DeleteFileToDir(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        path = HomeDisk + '/' + UserName + path

        if os.path.isdir(path):
            Methods.deleteDir(path)
            os.rmdir(path)
        else:
            FileDisk = path.split('/')[:-1]
            FileDisk = '/'.join(FileDisk)
            fileName = path.split('/')[-1]
            fileName = fileName.split('.')[0] if fileName.split('.') else fileName
            FileDiskCover = FileDisk + '/$cover.Img/cover_'+ fileName +'.jpg'
            if os.path.exists(FileDiskCover):
                os.remove(FileDiskCover)
            os.remove(path)
        return JsonResponse({'code':200, 'msg': '删除成功'})


class createDir(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        dirName = PostData['dirName']
        path = HomeDisk + '/' + UserName + path + '/' + dirName
        os.makedirs(path)
        return JsonResponse({'code': 200, 'msg': '创建成功'})


class createFile(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        fileName = PostData['dirName']
        path = HomeDisk + '/' + UserName + path + '/' + fileName
        file = open(path, 'w')
        file.close()
        return JsonResponse({'code': 200, 'msg': '创建成功'})

class moveDir_file(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        # dirName = PostData['fileName']
        OldPath = PostData['oldPath']
        OldPath = HomeDisk + '/' + UserName + OldPath
        NewPath = HomeDisk + '/' + UserName + PostData['NewPath']
        # print(OldPath, NewPath)
        shutil.move(OldPath, NewPath)
        return JsonResponse({'code': 200, 'msg': '移动成功'})

# 阿里云oss
class ReadOSS_Dir(APIView):
    def get(self, request):
        token = request.headers
        # Usertoken = token['Token']
        # UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        auth = oss2.Auth('', '')
        bucket = oss2.Bucket(auth, '', '')
        get_route = request.GET.get('route')
        if get_route == '/':
            get_route = ''
        else:
            get_route = get_route[1:] + '/'

        DiskDic = Methods.ReadOss_Dir(bucket, get_route)

        return JsonResponse(DiskDic)

class Read_OSSdisk(APIView):
    def get(self, request):
        dirPath = request.GET.get('route')
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        # print(get_route)

        auth = oss2.Auth('', '')
        bucket = oss2.Bucket(auth, '', '')
        get_route = request.GET.get('route')

        if get_route == '/':
            get_route = ''
        elif get_route[:1] == '/':
            get_route = get_route[1:] + '/'
        DiskDic = Methods.ReadOss_Dir(bucket, get_route, mode=2)
        # print(get_route)
        dir_list = []
        for i in DiskDic['dir']:

            # print(i['path'])
            dic = {
                'name': i['data'],
                'path': i['path']
            }
            dir_list.append(dic)
        return JsonResponse({'code': 200, 'data': dir_list})


class DeleteOssFileToDir(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        T = PostData['t']
        if path[:1] == '/':
            path = path[1:]


        auth = oss2.Auth('', '')
        bucket = oss2.Bucket(auth, '', '')
        if T == 'dir':
            for obj in oss2.ObjectIterator(bucket, prefix=path):
                bucket.delete_object(obj.key)
        else:
            bucket.delete_object(path)
        return JsonResponse({'code':200, 'msg': '删除成功'})


class createOssDir(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        path = PostData['path']
        if path[:1] == '/':
            path = path[1:]

        dirName = PostData['dirName']

        auth = oss2.Auth('', '')
        bucket = oss2.Bucket(auth, '', '')

        bucket.put_object(path + '/' + dirName+'/', '')
        return JsonResponse({'code': 200, 'msg': '创建成功'})

class moveOssDir_file(APIView):
    @csrf_exempt
    def post(self, request):
        token = request.headers
        Usertoken = token['Token']
        UserName = UserToken.objects.get(token=Usertoken).user.user_Disk
        PostData = (json.loads(request.body))
        # dirName = PostData['fileName']
        OldPath = PostData['oldPath']
        NewPath = PostData['NewPath']
        if OldPath[:1] == '/':
            OldPath = OldPath[1:]
        fileName = OldPath.split('/')[-1]
        NewPath = NewPath + fileName


        bucket_name = 'awowyao'

        auth = oss2.Auth('', '')
        bucket = oss2.Bucket(auth, '', '')
        # 填写不包含Bucket名称在内源Object的完整路径，例如srcexampleobject.txt。
        src_object_name = OldPath
        # 填写不包含Bucket名称在内目标Object的完整路径，例如destexampleobject.txt。
        dest_object_name = NewPath
        # 获取源文件的大小。当在同一个Bucket内拷贝文件时，请将src_bucket改为bucket。
        head_info = bucket.head_object(src_object_name)
        total_size = head_info.content_length
        print('src object size:', total_size)

        # determine_part_size方法用来确定分片大小。
        part_size = oss2.determine_part_size(total_size, preferred_size=500 * 1024)
        # 初始化分片。
        upload_id = bucket.init_multipart_upload(dest_object_name).upload_id
        parts = []

        # 逐个上传分片。
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            end = offset + num_to_upload - 1

            result = bucket.upload_part_copy(bucket_name, src_object_name, (offset, end), dest_object_name,
                                             upload_id, part_number)
            # 保存part信息。
            parts.append(oss2.models.PartInfo(part_number, result.etag))

            offset += num_to_upload
            part_number += 1

        # 完成分片拷贝。
        result = bucket.complete_multipart_upload(dest_object_name, upload_id, parts)

        if result.status == 200:
            bucket.delete_object(src_object_name)

        return JsonResponse({'code': 200, 'msg': '移动成功'})



# 系统管理监控
import psutil, time
class SystemMonitorApi(APIView):
    def get(self, request):

        dic = {}
        # 当前网络和总体网络
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        read_bytes = psutil.disk_io_counters().read_bytes  # 硬盘读io
        write_bytes = psutil.disk_io_counters().write_bytes  # 硬盘写io
        time.sleep(1)
        read_now = psutil.disk_io_counters().read_bytes  # 硬盘读io
        write_now = psutil.disk_io_counters().write_bytes  # 硬盘写io
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        sent = (sent_now - sent_before)  # 算出1秒后的差值
        recv = (recv_now - recv_before)
        read = (read_now - read_bytes)
        write = (write_now - write_bytes)
        dic['nowSentSun'] = [sent_before]
        dic['nowRecvtSun'] = sent_before
        dic['time_start'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dic['time_end'] = (datetime.datetime.now() + datetime.timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S")
        dic['sent'] = [dic['time_start'], format(int(sent) / 1024, '.2f')]
        dic['recv'] = [dic['time_start'], format(int(recv) / 1024, '.2f')]
        dic['read'] = [dic['time_start'], format(int(read) / 1024, '.2f')]
        dic['write'] = [dic['time_start'], format(int(write) / 1024, '.2f')]
        dic['diskType'] = 'kb'
        # cpu温度
        SystemTem = os.popen('sensors').read()
        SystemTem0 = re.findall('id 0.*?\+(.*?)\(high', SystemTem)[0]
        dic['cpuTem'] = re.sub('°C', '', SystemTem0)
        # cpu的使用率
        cup_per = psutil.cpu_percent(interval=0.5)  # 0.5刷新频率
        dic['cupPer'] = cup_per
        # 内存信息(内存利用率)
        memory_info = psutil.virtual_memory().percent
        dic['memoryInfo'] = memory_info
        wifi_LOG = ''
        # wifi连接日志
        return JsonResponse(dic)