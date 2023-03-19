from datetime import datetime
from gc import collect
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
    
    def get_status(self):
        bills = Collectible.objects.select_related('reading').filter(reading__user = self, status = 'paid')

        if bills:
            return 'paid'
        return 'unpaid'
        

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    message = models.TextField(blank=False, null=True)
    status = models.CharField(blank = False, null= False, max_length=12)
    created_on = models.DateTimeField(null=True, blank=True, default=datetime.now)
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    content = models.TextField(blank=False, null=True)
    link = models.CharField(blank=False, null=False, max_length=60)
    status = models.IntegerField(choices = ((0, 'Unseen'), (1, 'Seen')))
    created_on = models.DateTimeField(null=True, blank=True, default=datetime.now)
    
    def __str__(self):
        return self.content

class Reading(models.Model):
    previous = models.IntegerField(blank = False, null= False)
    present = models.IntegerField(blank = False, null = False)
    billing_month = models.DateField(null=True, blank=True)
    consumption = models.IntegerField(blank = False, null=False)
    multiplier = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return self.consumption
    
class Collectible(models.Model):
    penalty = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    amount = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    due_date = models.DateField(blank = False, null = False, max_length = 32)
    status = models.CharField(blank = False, null = False, max_length = 32)
    reading = models.OneToOneField(Reading, on_delete = models.DO_NOTHING, null = True)

    def __str__(self):
        return str(self.amount)

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    amount = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    tendered = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    change = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    order_number = models.CharField(max_length=120, default='ABCD-1234')
    content = models.TextField(blank=False, null=True)
    created_on = models.DateTimeField(null=True, blank=True, default=datetime.now)

class Invoice(models.Model):
    collectible = models.OneToOneField(Collectible, on_delete = models.DO_NOTHING, null = True)
    transaction = models.ForeignKey(Transaction, on_delete = models.DO_NOTHING, null = True)
    