from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Sum, Min, Value

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
    consumption = models.IntegerField(blank = False, null=False)
    multiplier = models.DecimalField(blank = False, null=False, decimal_places=2, max_digits=32)
    user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return f'{self.consumption}'
    
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
    expected_income = models.DecimalField( max_digits=15, decimal_places=2, help_text="in pesos")
    
    def consumed_water(self):
        consumed = Reading.objects.filter(billing_month=self.month).aggregate(consumed=Sum('consumption'))
        return consumed.get('consumed')    
    
    def water_loss(self):
        loss = self.released_water - self.consumed_water()
        return loss if loss > 0 else 0
    
    def collected(self):
       collection = Transaction.objects.filter(created_on__month=self.month.month).aggregate(collection=Sum('amount'))
       collected = collection.get('collection') if collection.get('collection') else 0
       return collected
        
    def deficit(self):
       collection = Transaction.objects.filter(created_on__month=self.month.month).aggregate(collection=Sum('amount'))
       collected = collection.get('collection') if collection.get('collection') else 0
       result = self.expected_income - collected
       return result if result > 0 else 0
   
    def status(self):
        return 'Accomplished' if self.deficit() <= 0 else 'Unaccomplished'