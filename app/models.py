from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class Employees(User):
    name=models.CharField(max_length=100)
    role=models.CharField(max_length=50)
    contact_no=models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Employees'

class Tax_rate(models.Model):
    tax_name=models.CharField(max_length=50)
    tax_percent=models.IntegerField()
    class Meta:
        db_table = 'Tax_rate'
    def __str__(self):
        return self.tax_percent
class Room_type(models.Model):
    type=models.CharField(max_length=50)
    area=models.IntegerField()
    price=models.FloatField(default=1000)
    tax_name=models.ForeignKey(Tax_rate,on_delete=models.CASCADE)
    def __str__(self):
        return self.type
    class Meta:
        db_table = 'Room_types'


class Room_pricing(models.Model):
    room_type=models.OneToOneField(Room_type,on_delete=models.CASCADE)
    price=models.IntegerField()
    last_changed_on=models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Room_pricing'

class Room_features(models.Model):
    room_type=models.OneToOneField(Room_type,on_delete=models.CASCADE,related_name='features')
    standard=models.CharField(max_length=50)
    feature=models.CharField(max_length=200)
    updated_on=models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Room_features'

class Rooms(models.Model):
    room_type=models.ForeignKey(Room_type,on_delete=models.CASCADE,)
    room_number=models.IntegerField(primary_key=True)
    price=models.IntegerField()
    def __str__(self):
        return f"Room {self.room_number}" 
    class Meta:
        db_table = 'Rooms'

class Room_images(models.Model):
    room_type=models.ForeignKey(Room_type,on_delete=models.CASCADE)
    image=models.ImageField()
    class Meta:
        db_table = 'Room_images'
    def __str__(self):
        return str(self.room.room_number)+str("-")+str(self.id)
        
class customer(models.Model):
    name=models.CharField(max_length=100)
    contact_no=models.IntegerField()
    address=models.CharField(max_length=300)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Customer'

class Reservations(models.Model):
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    reserved_for=models.ForeignKey(customer,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    check_in_date=models.DateField()
    payment_status=models.BooleanField(default=False)
    check_out_date = models.DateField()
    reserved_by=models.ForeignKey(Employees,on_delete=models.DO_NOTHING,null=True)
    def __str__(self):
        return str(self.room)+' '+str(self.check_in_date)+' to '+str(self.check_out_date)
    class Meta:
        db_table = 'Reservations'

class Payments(models.Model):
    reservation=models.OneToOneField(Reservations,on_delete=models.CASCADE)
    amount=models.IntegerField()
    payment_mode=models.CharField(max_length=50)
    payment_status=models.CharField(max_length=50,default='not completed')
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Payments'

class Customer_Rating(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    rating=models.IntegerField()
    class Meta:
        db_table = 'Customer_Rating'
    
class Room_reviews(models.Model):
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    review=models.TextField()
    class Meta:
        db_table = 'Room_reviews'


class Room_pricing(models.Model):
    room_type=models.OneToOneField(Room_type,on_delete=models.CASCADE)
    price=models.IntegerField()
    class Meta:
        db_table = 'Room_pricing'

class Room_availability(models.Model):
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    is_available=models.BooleanField(default=True)
    date=models.DateField()
    class Meta:
        db_table = 'Room_availability'

class Reports(models.Model):
    reported_by=models.ForeignKey(Employees,on_delete=models.CASCADE)
    bug=models.TextField()
    reported_on=models.DateTimeField()
    class Meta:
        db_table = 'Reports'

class customer_personal_data(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    identifcation_number=models.IntegerField()
    verified=models.BooleanField()
    class Meta:
        db_table = 'customer_personal_data'