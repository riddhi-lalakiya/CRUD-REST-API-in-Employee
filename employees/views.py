# ***************** Django Libraries *****************
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect

# ***************** REST Lib *****************
from rest_framework.response import Response
from rest_framework import viewsets, status, filters

# ***************** Models *****************
from employees.models import *
from employees.serializers import *



# Create your views here.
# ***************** REST APIS *****************
class ProjectList(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    # queryset = Project.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['project_name']
    ordering_fields = ['project_name']

    def get_queryset(self):
        project_obj = Project.objects.all()
        return project_obj

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ProjectUpdate(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = 'id'

    def get_queryset(self):
        project_obj = Project.objects.filter(id=self.kwargs['id'])
        return project_obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destory(self,request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerList(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['customer_name','=customer_phone_number','customer_address']

    def get_queryset(self):
        customer_obj = Customer.objects.all()
        return customer_obj

    def list(self, request, *args, **kwargs):
        queryset = Customer.objects.all()
        serializer =self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CustomerUpdate(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    lookup_field ='id'
    #queryset = Customer.objects.all()

    def get_queryset(self):
        customer_obj = Customer.objects.filter(id=self.kwargs['id'])
        return customer_obj

    def retrieve(self, request, *args, **kwargs):
        customer_obj = Customer.objects.get(id=kwargs['id'])
        serializer = self.get_serializer(customer_obj)
        return Response(serializer.data)    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destory(self,request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    

# ***************** END REST APIS *****************

def signin(request):
    if request.method == 'GET':
        template_name = 'signin.html'
        return render(request,template_name)

    if request.method == 'POST':
        template_name = 'signin.html'
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password):
            return render(request,template_name, {'error': 'Invalid email or password...!'})
            
        else:
            user = authenticate(username = email, password = password)
            if user is not None and user.is_active:
                login(request, user)
                if request.POST.get("next", None):
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return redirect("employees:dashboard")
            else:
                return render(request,template_name,{'error': 'Invalid email or password...!'})

def signup(request):
    if request.method == "GET":
        template_name = 'signup.html'
        reporting_managers = EmployeeProfile.objects.filter(designation='1')
        return render(request,template_name, {'reporting_managers': reporting_managers})
    
    if request.method == "POST":
        template_name = 'signup.html'

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        reporting_manager = request.POST.get('reporting_manager')

        crete_password = make_password(password)

        try:
            user_obj = User.objects.get(username=email)
            return render(request,template_name, {'error': 'Email already exits..!'})

        except User.DoesNotExist:
            user_obj = User.objects.create(
                username = email,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = crete_password,
            )

            if len(reporting_manager)>0:
                rp_manager = User.objects.get(id=reporting_manager)
            else:
                rp_manager = None

            try:
                emp_profile_obj = EmployeeProfile.objects.create(
                    user = user_obj,
                    phone_number = phone_number,
                    address1 = address_1,
                    address2 = address_2,
                    city = city,
                    state = state,
                    country = country,
                    pincode = pincode,
                    designation = designation,
                    department = department,
                    reporting_manager = rp_manager,
                )
                return redirect("employees:signin")
            
            except Exception as e:
                print(e)
                return render(request,template_name, {'error': e})

@login_required(login_url='/')
def signout(request):
    logout(request)
    return redirect("employees:signin")

@login_required(login_url='/')
def dashboard(request):
    template_name = 'employees/dashboard.html'
    pm_profiles = None
    if request.user.employeeprofile.designation == '3':
        pm_profiles = EmployeeProfile.objects.filter(designation='1')
    if request.user.employeeprofile.designation == '2':
        emp_profiles = EmployeeProfile.objects.filter(user = request.user)
    else:
        emp_profiles = EmployeeProfile.objects.filter(designation='2')
    return render(request,template_name, {'emp_profiles': emp_profiles, 'pm_profiles': pm_profiles, 'nav_dashboard': "active"})

@login_required(login_url='/')
def updateDetail(request, user_id):

    if request.method == 'GET':
        template_name = 'employees/update_employee_details.html'
        reporting_managers = EmployeeProfile.objects.filter(designation='1')

        if request.user.employeeprofile.designation != '2':
            try:
                emp_obj = User.objects.get(id=user_id)
                emp_profile_obj = EmployeeProfile.objects.get(user=emp_obj)
                return render(request,template_name, {'emp_detail': emp_obj, 'reporting_managers':reporting_managers, 'emp_profile':emp_profile_obj})
            except:
                return redirect('employees:dashboard')
        else:
            return redirect('employees:dashboard')
    
    if request.method == 'POST':
        template_name = 'employees/update_employee_details.html'

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        reporting_manager = request.POST.get('reporting_manager')

        if len(reporting_manager)>0:
            rp_manager = User.objects.get(id=reporting_manager)
        else:
            rp_manager = None

        try:
            user_obj = User.objects.get(id=user_id)
            emp_profile_obj = EmployeeProfile.objects.get(user=user_obj)
            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.save()

            emp_profile_obj.phone_number = phone_number
            emp_profile_obj.address1 = address_1
            emp_profile_obj.address2 = address_2
            emp_profile_obj.city = city
            emp_profile_obj.state = state
            emp_profile_obj.country = country
            emp_profile_obj.pincode = pincode
            emp_profile_obj.designation = designation
            emp_profile_obj.department = department
            emp_profile_obj.reporting_manager = rp_manager

            emp_profile_obj.save()
            return redirect('employees:dashboard')
        except:
            return redirect('employees:dashboard')

@login_required(login_url='/')
def addDetail(request):
    if request.method == 'GET':
        template_name = 'employees/add_employee_details.html'
        reporting_managers = EmployeeProfile.objects.filter(designation='1')
    
        if request.user.employeeprofile.designation != '2':
            return render(request,template_name, {'reporting_managers':reporting_managers})
        else:
            return redirect("employees:dashboard")
        
    if request.method == 'POST':
        template_name = 'employees/add_employee_details.html'

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        reporting_manager = request.POST.get('reporting_manager')

        crete_password = make_password(password)

        try:
            user_obj = User.objects.get(username=email)
            return render(request,template_name, {'error': 'Email already exits..!'})

        except User.DoesNotExist:
            user_obj = User.objects.create(
                username = email,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = crete_password,
            )

            if len(reporting_manager)>0:
                rp_manager = User.objects.get(id=reporting_manager)
            else:
                rp_manager = None

            try:
                emp_profile_obj = EmployeeProfile.objects.create(
                    user = user_obj,
                    phone_number = phone_number,
                    address1 = address_1,
                    address2 = address_2,
                    city = city,
                    state = state,
                    country = country,
                    pincode = pincode,
                    designation = designation,
                    department = department,
                    reporting_manager = rp_manager,
                )
                return redirect("employees:dashboard")
            
            except Exception as e:
                print(e)
                return render(request,template_name, {'error': e})

@login_required(login_url='/')
def changePassword(request):
    if request.method == 'GET':
        template_name = 'employees/change_password.html'
        return render(request,template_name, {"nav_change_password": "active"})

    if request.method == 'POST':
        template_name = 'employees/change_password.html'
        password = request.POST.get('password')
        changepassword = request.POST.get('changepassword')

        if password == changepassword:
            user_obj = User.objects.get(id = request.user.id)
            user_obj.password = make_password(password)
            user_obj.save()
            return redirect("employees:signout")
        return render(request,template_name,{'error':'Password and Confirm Password doesn\'t match..!'})