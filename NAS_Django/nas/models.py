from django.db import models

# Create your models here.
class users_table(models.Model):
    user_name = models.CharField(max_length=255)
    user_pwd = models.CharField(max_length=255)
    user_nickname = models.CharField(max_length=255, null=True)
    user_cover = models.CharField(max_length=255, null=True)
    user_sex = models.CharField(max_length=4, null=True)
    user_email = models.EmailField(null=True)
    user_Disk = models.CharField(max_length=40)
    user_disk_size = models.CharField(max_length=40)
    user_Mobile = models.CharField(max_length=16,null=True)
    user_address = models.CharField(max_length=255, null=True)
    user_sign_time = models.CharField(max_length=50)
    user_last_login = models.CharField(max_length=255, null=True)
    user_lv = models.IntegerField(default=1)
    user_lv_msg = models.TextField(null=True)
    user_oss_msg = models.TextField(null=True)
    user_QBdownload_List = models.TextField(null=True)
    user_download_speed = models.IntegerField(default=200)




class UserCode(models.Model):
    user = models.OneToOneField(users_table, on_delete=models.CASCADE)
    commonlyCode = models.CharField(max_length=10, null=True)
    time = models.DateTimeField('创建时间', auto_now_add=True)

class UserToken(models.Model):
    user = models.OneToOneField(users_table, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    time = models.DateTimeField('创建时间', auto_now_add=True)