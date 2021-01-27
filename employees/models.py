from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

# Create your models here.
class EmployeeProfile(models.Model):

    designation_choices = [
        ('1', 'Project Manager'),
        ('2', 'Employee'),
        ('3', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(null=True,unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    address1 = models.CharField(max_length=255, null=False)
    address2 = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=10, null=False)
    state = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=10, null=False)
    pincode = models.IntegerField(default=0)
    designation = models.CharField(max_length=4, null=False, choices=designation_choices, default='2')
    department = models.CharField(max_length=50, null=False)
    reporting_manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="reporting_manager")

    def __str__(self):
        return self.user.get_full_name()

class Customer(models.Model):
    customer_name = models.CharField(max_length=50, null=False)
    customer_phone_number = models.CharField(null=True,unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    customer_address = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    

class Project(models.Model):
    project_name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    





