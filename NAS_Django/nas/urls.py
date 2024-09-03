from django.urls import path
from .views import *

urlpatterns_1 = [
    # path("index", AL_yun),
    # path("GetGoute", ReadOSS_Dir.as_view()),
    path("GetGoute", Read_Dir.as_view()),
    path('upload', Up_Data.as_view()),
    path('setQbittor', setQbittor.as_view()),
    path('GetDisk', Read_disk.as_view()),
    path('getQbDownloadData', getQbDownloadData.as_view()),
    path('ControlQb', ControlQbDownload.as_view()),
    path('DeleteFileToDir', DeleteFileToDir.as_view()),
    path('createDir',createDir.as_view()),
    path('createFile', createFile.as_view()),
    path('moveDirFile', moveDir_file.as_view()),
    path('GetFileText', GetFileText.as_view()),
    path('setFileText', setFileText.as_view()),
]

urlpatterns_2 = [
    path('userApi/Login', UserLogin.as_view()),
    path('userApi/Sign', UserSign.as_view()),
    path('userApi/GetUserMsg', GetUserMsg.as_view()),
    path('User/checkUser', checkUser),
    path('User/GetUsersManage',GetUsersManage.as_view()),
    path('User/DeleteUserManage',DeleteUserManage.as_view()),
    path('userApi/UpUserManage',UpUserManage.as_view())
]

urlpatterns_3 = [
    path('sys/GetSize', Get_Disk_Size.as_view()),
    path('sys/SystemMonitorApi', SystemMonitorApi.as_view())
]

# 阿里云OSS
urlpatterns_4 = [
    path('Oss/GetGoute', ReadOSS_Dir.as_view()),
    path('Oss/GetDisk', Read_OSSdisk.as_view()),
    path('Oss/DeleteUserManage', DeleteOssFileToDir.as_view()),
    path('Oss/createDir', createOssDir.as_view()),
    path('Oss/moveDirFile', moveOssDir_file.as_view()),

]

urlpatterns = urlpatterns_1 + urlpatterns_2 + urlpatterns_3 + urlpatterns_4