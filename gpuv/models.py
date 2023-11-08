from django.db import models
from django.contrib.auth.models import User


    
class Vmlist(models.Model):
    vm_name = models.CharField(max_length=100)
    ipaddr = models.CharField(max_length=20)
    rootname = models.CharField(max_length=50)
    rootpass = models.CharField(max_length=20) 
    def __str__(self):
        return self.vm_name
    
class UserVm(models.Model):
    user_choice = models.ForeignKey(User, on_delete=models.CASCADE, default = 0)
    vm_choice = models.ForeignKey(Vmlist, on_delete=models.CASCADE,  default = 0)
    accountname = models.CharField(max_length=50)
    accountpass = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user_choice.username} - {self.vm_choice.vm_name}"