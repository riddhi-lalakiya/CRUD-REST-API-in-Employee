from django.urls import path
from employees.views import *


app_name = "employees"

urlpatterns = [
    path('', signin, name="signin"),
    path('signup', signup, name="signup"),
    path('signout', signout, name="signout"),
    path('dashboard', dashboard, name="dashboard"),

    path('<int:user_id>/edit', updateDetail, name="update_emp_details"),
    path('add', addDetail, name="add_emp_details"),
    path('change-password', changePassword, name='change_password'),

    # ***************** REST APIS *****************
    path('projects', ProjectList.as_view({"get":"list","post":"create"})),
    path('project/<int:id>', ProjectUpdate.as_view({"get":"retrieve","put":"update","delete":"destroy"})),

    path('customers', CustomerList.as_view({"get":"list","post":"create"})),
    path('customer/<int:id>', CustomerUpdate.as_view({"get":"retrieve","put":"update","delete":"destroy"})),
    # **************************************************** #

    
    
]