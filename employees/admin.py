from django.contrib import admin
from employees.models import *

# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Project)
admin.site.register(Customer)
