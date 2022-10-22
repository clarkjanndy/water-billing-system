from django.db import models
from django.contrib.auth.models import AbstractUser

class Baranggay(models.Model):
    name = models.CharField(max_length = 50, blank = False)
    code = models.CharField(max_length = 50, blank = True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    meter_no = models.CharField(max_length=50, blank = False)
    middle_name = models.CharField(max_length=50, blank = True)
    ext_name = models.CharField(max_length=50, blank = True)
    gender = models.CharField(null = False, blank = False, max_length = 32)
    civil_status = models.CharField(null = False, blank = False, max_length = 32)
    address = models.ForeignKey(Baranggay, on_delete=models.DO_NOTHING, null = True)
    religion = models.CharField(null = False, blank = False, max_length = 32)
    contact_no = models.CharField(max_length=50, blank = True, default = '09')    
    
    def __str__(self):
        return self.username
    
class Notification(models.Model):
    content = models.TextField(blank=False)
    user = models.OneToOneField(CustomUser, on_delete = models.DO_NOTHING)
    status = models.IntegerField(choices = ((0, 'Unseen'), (1, 'Seen')))
    
    def __str__(self):
        return self.content

class Reading(models.Model):
    previous = models.IntegerField(blank = False, null= False)
    present = models.IntegerField(blank = False, null = False)
    billing_month = models.DateField(auto_now_add=True, blank=True)
    consumption = models.IntegerField(blank = False, null=False)
    multiplier = models.IntegerField(blank = False, null=False)
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return self.consumption
    
class Collectibles(models.Model):
    category = models.IntegerField(blank = False, null = False)
    amount = models.BigIntegerField(blank = False, null = False)
    due_date = models.DateField(blank = False, null = False, max_length = 32)
    status = models.IntegerField(blank = False, null = False)
        