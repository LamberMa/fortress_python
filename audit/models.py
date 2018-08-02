from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class IDC(models.Model):
    name = models.CharField(max_length=, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """
    存储主机信息
    hostname:
    ip_addr: 主机的ip地址
    port: 主机的端口
    idc:
    enabled:
    """
    hostname = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey('IDC', on_delete=models.CASCADE)
    host_users = models.ManyToManyField("HostUser")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" % (self.hostname, self.ip_addr)


class HostGroup(models.Model):
    # 主机组
    name = models.CharField(max_length=64, unique=True)
    host_user_binds = models.ManyToManyField("HostUserBind")


class HostUser(models.Model):
    """
    存储远程主机的用户信息
    username:
    password:密码这应该存储明文，因为ssh的时候接受的密码就是明文，这样的设计里只能存储明文
    """
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s" % (self.get_auth_type_display(), self.username, self.password)

    class Meta:
        unique_together = ('username', 'password')


class HostUserBind(models.Model):
    """
    绑定主机和用户的明细
    """
    host = models.ForeignKey("Host", on_delete=models.CASCADE)
    host_user = models.ForeignKey("HostUser", on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s" %(self.host, self.host_user)

    class Meta:
        unique_together = ('host', 'host_user')



class AuditLog(models.Model):
    # 审计日志
    pass


class Account(models.Model):
    """
    堡垒机账户，可以分给用户主机组，或者单独的主机
    1、扩展
    2、继承
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    # 针对于多对多，如果不想填，直接写blank为True就行了，不需要None=True
    hosts_user_binds = models.ManyToManyField('HostUserBind', blank=True)
    host_groups = models.ManyToManyField("HostGroup", blank=True)

    def __str__(self):
        return self.name

