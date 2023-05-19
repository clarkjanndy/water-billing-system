from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Sum, Min, Value
from decimal import Decimal

from django.core.exceptions import ValidationError

from django.utils import timezone

from .utils.constants import dummy_text

class Baranggay(models.Model):
    name = models.CharField(max_length = 50, blank = False)
    code = models.CharField(max_length = 50, blank = True)
    description = models.TextField(blank=True, default=dummy_text)
    
    def __str__(self):
        return self.name
    
    def consumer_count(self):
        count = CustomUser.objects.filter(address=self, is_superuser = 0).aggregate(count=Count(id)).get('count')
        return count
    
    def collected(self):
        consumers = CustomUser.objects.all().filter(address=self, is_superuser = 0)
        collection = Transaction.objects.filter(user__in = consumers).aggregate(collection=Sum('amount')).get('collection')
        return collection
    
    def consumed_water(self):
        consumers = CustomUser.objects.all().filter(address=self, is_superuser = 0)
        consumption = Reading.objects.filter(user__in = consumers).aggregate(consumption=Sum('consumption')).get('consumption')
        return consumption
    
class CustomUser(AbstractUser):
    meter_no = models.CharField(max_length=50, blank = False)
    middle_name = models.CharField(max_length=50, blank = True)
    ext_name = models.CharField(max_length=50, blank = True)
    gender = models.CharField(null = False, blank = False, max_length = 32)
    civil_status = models.CharField(null = False, blank = False, max_length = 32)
    address = models.ForeignKey(Baranggay, on_delete=models.DO_NOTHING, null = True)
    religion = models.CharField(null = False, blank = False, max_length = 32)
    contact_no = models.CharField(max_length=50, blank = True, default = '09')    
    registration_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.ext_name}'
    
    @property
    def get_status(self):
        bills = Collectible.objects.select_related('reading').filter(reading__user = self, status = 'unpaid')

        if bills:
            return 'unpaid'
        
        return 'paid'
    
    @property
    def get_latest_bill(self):
        collectible = Collectible.objects.select_related("reading").filter(reading__user_id=self.id).order_by("-reading__billing_month").first()
        
        if not collectible:
            return 0
              
        return collectible.id
        

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
    consumption = models.DecimalField(blank = False, null=False,  max_digits=15, decimal_places=2)
    multiplier = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return f'{self.consumption}'
    
    def save(self, *args, **kwargs):
        query_projection = Projection.objects.filter(month = self.billing_month)
    
        if query_projection:
            projection = query_projection.first()
            projection.remaining_water = projection.remaining_water - Decimal(self.consumption)
            projection.save()
        
        return super(Reading, self).save(*args, **kwargs)
    
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

class Projection(models.Model):
    month = models.DateField()
    released_water = models.DecimalField( max_digits=15, decimal_places=2, help_text="in cm3")
    remaining_water = models.DecimalField( max_digits=15, decimal_places=2, help_text="in cm3", default = 0)
    expected_income = models.DecimalField( max_digits=15, decimal_places=2, help_text="in pesos")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if Decimal(self.released_water) < self.consumed_water():
                raise ValidationError('Released water must be greater than or equal to consumed')
            
            self.remaining_water = Decimal(self.released_water) - self.consumed_water() #calculate remaning here
        return super(Projection, self).save(*args, **kwargs)
    
    def consumed_water(self):
        consumed = Reading.objects.filter(billing_month=self.month).aggregate(consumed=Sum('consumption'))
        return consumed.get('consumed') if consumed.get('consumed') else 0
    
    def water_loss(self):         
        if Decimal(self.remaining_water) >= self.consumed_water():
            return 0
        
        return self.consumed_water() - Decimal(self.remaining_water)
    
    def collected(self):
       collection = Transaction.objects.filter(created_on__month=self.month.month).aggregate(collection=Sum('amount'))
       return collection.get('collection') if collection.get('collection') else 0
        
    def deficit(self):
       result = self.expected_income - self.collected()
       return result if result > 0 else 0
   
    def status(self):
        return 'Accomplished' if self.deficit() <= 0 else 'Unaccomplished'
    
    def transactions(self):
        transactions = Transaction.objects.filter(created_on__month=self.month.month)
        return transactions if  transactions else []
    
    def readings(self):
        readings = Reading.objects.filter(billing_month=self.month)
        return readings if readings else []
    
class Setting(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='setting_author')
    name = models.CharField(max_length=225)
    variable = models.CharField(max_length=225)
    value = models.TextField()
    
    def __str__(self):
        return f'{self.variable} - {self.value}'