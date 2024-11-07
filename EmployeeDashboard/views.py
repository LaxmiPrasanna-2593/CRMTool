from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import User

def signup_view(request):
    if request.method == 'POST':
        # Manually retrieve data from the POST request
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        department = request.POST.get('department')
        
        # Basic validation
        if not username or not password1 or not password2 or not department:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        # Create and save the user
        user = User(username=username, password=make_password(password1), department=department)
        user.save()

       # Inform the user of successful registration
        messages.success(request, "User created successfully! User can now log in.")
        
        # Redirect to the signup page or login page (depending on your flow)
        return redirect('signup')  # Change this to 'login' if you prefer to redirect to login page
    
    
    # Display signup page
    return render(request, 'signup.html', {
        'department_choices': User.DEPARTMENT_CHOICES
    })

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

from django import forms
from .models import TLTasks
@login_required
def dashboard_view(request):
    user_department = request.user.department
    context = {}

    if request.user.is_superuser:
        return render(request, 'dashboard.html')

    if user_department == 'teamlead_development':
        tasks = Task.objects.filter(assigned_to='Dev_TL').order_by('due_date')
        context['tasks'] = tasks
        return render(request, 'development_dashboard.html', context)
    elif user_department == 'teamlead_content_moderators':
        tasks = Task.objects.filter(assigned_to='Content_TL').order_by('due_date')
        context['tasks'] = tasks
        return render(request, 'content_moderator_dashboard.html', context)
    elif user_department == 'teamlead_sales_team':
        tasks = Task.objects.filter(assigned_to='Sales_TL').order_by('due_date')
        context['tasks'] = tasks
        return render(request, 'sales_team_dashboard.html', context)
    elif user_department == 'teamlead_customer_support':
        tasks = Task.objects.filter(assigned_to='Support_TL').order_by('due_date')
        context['tasks'] = tasks
        return render(request, 'customer_support_dashboard.html', context)
    else:
        # For employees, display tasks assigned to the logged-in user and allow status updates
        user_tasks = TLTasks.objects.filter(assigned_to=request.user.username).order_by('due_date')
        if request.method == "POST":
            task_id = request.POST.get("task_id")
            task = get_object_or_404(TLTasks, id=task_id)
            form = TLTaskStatusForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            form = TLTaskStatusForm()
        
        context['user_tasks'] = user_tasks
        context['form'] = form
        return render(request, 'employee_dashboard.html', context)

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def custom_logout_view(request):
    logout(request)  # Log out the current user
    messages.info(request, "You have been logged out.") 
    return redirect('login')  


from django.shortcuts import render, redirect
from .forms import EmployeeForm, TLTaskStatusForm

def employee_form_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_success')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})



def employee_success_view(request):
    return render(request, 'employee_sucess.html')  # Render the success template


from django.shortcuts import render, get_object_or_404
from .models import Employee
from django.urls import reverse

# View to list all employees
def employee_list(request):
    employees = Employee.objects.all()
    total_count = employees.count()
    active_count = employees.filter(employee_status='Active').count()
    inactive_count = employees.filter(employee_status='InActive').count()
    
    context = {
        'employees': employees,
        'total_count': total_count,
        'active_count': active_count,
        'inactive_count': inactive_count,
    }
    
    return render(request, 'employee_list.html', context)

# View to show details of a specific employee
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('employee_detail', args=[employee.pk]))
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form, 'employee': employee})
 
from django.shortcuts import render, redirect
from .models import Lead
from .forms import LeadForm

# View to display the list of leads
def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'lead_list.html', {'leads': leads})

# View to create a new lead
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})

def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'lead_detail.html', {'lead': lead})

def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'lead_form.html', {'form': form, 'lead': lead})    

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# View to list all tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# View to create a new task (only accessible by admin users)
@login_required
def task_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to create tasks.")
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user.username  # Set the logged-in user as the creator
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {'form': form})

# View to edit an existing task
@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from .models import TLTasks
from .forms import TLTaskForm

def tl_task_list(request):
    tasks = TLTasks.objects.all()
    return render(request, 'tl_task_list.html', {'tasks': tasks})

def tl_task_create(request):
    if request.method == 'POST':
        form = TLTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tl_task_list')
    else:
        form = TLTaskForm()
    return render(request, 'tl_task_form.html', {'form': form, 'action': 'Create'})

def tl_task_edit(request, task_id):
    task = get_object_or_404(TLTasks, id=task_id)
    if request.method == 'POST':
        form = TLTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tl_task_list')
    else:
        form = TLTaskForm(instance=task)
    return render(request, 'tl_task_form.html', {'form': form, 'action': 'Edit'})


from django.shortcuts import render
from .models import TLTasks

def admin_task_list_view(request):
    tasks = TLTasks.objects.all()  # Fetch all tasks from the database
    return render(request, 'admin_task_list.html', {'tasks': tasks})


from django.shortcuts import render
from .models import TLTasks
from django.contrib.auth.decorators import login_required

@login_required
def tlassigned_task_list_view(request):
    current_user = request.user.username
    tasks = TLTasks.objects.filter(assigned_by=current_user).order_by('due_date')
    
    context = {
        'tasks': tasks
    }
    
    return render(request, 'tl_assigned_task_list.html', context)
