from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class AgentInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(max_digits=10, default=0, decimal_places=9)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class UserInfo(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(max_digits=10, default=0, decimal_places=9)
    birth_date = models.DateField(null=True, blank=True)
    fb_id = models.CharField(max_length=255, null=True, blank=True)
    user_data = models.TextField(default='{}')

    def __str__(self):
        return self.fb_id

class Conversations(models.Model):

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(AgentInfo, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(default='{}')

    def __str__(self):
        return self.message

class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class InsuranceType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Addons(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_type = models.SmallIntegerField(default=0) # 0=bike, 1=car
    vehicle_price = models.IntegerField(default=500000)
    model_code = models.CharField(max_length = 255, null=True, blank=True)
    addons = models.ManyToManyField(Addons, related_name='available_addons')

    def __str__(self):
        return self.model_code

class Insurance(models.Model):

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    status = models.SmallIntegerField(default=0) # 0=Not activate, 1=Active, 2=Expired
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    premium = models.IntegerField(null=True, blank=True)
    idv = models.IntegerField(null=True, blank=True)
    insurance_type = models.ManyToManyField(InsuranceType, related_name='insurance_type')
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    addons = models.ManyToManyField(Addons, related_name='choosed_addons')

    def __str__(self):
        return self.user


class Schedule(models.Model):

    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, null=True, blank=True)
    agent = models.ForeignKey(AgentInfo, on_delete=models.CASCADE, null=True, blank=True)
    insurance = models.OneToOneField(Insurance, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    purpose = models.CharField(max_length = 255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.user.username
