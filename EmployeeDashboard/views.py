from django.conf import settings
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
from .models import TLTasks, Attendance, Leave
from .forms import TLTaskStatusForm

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
        user_attendance = Attendance.objects.filter(user=request.user).order_by('-date')
        user_leaves = Leave.objects.filter(user=request.user).order_by('-start_date') 

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
        context['attendance'] = user_attendance
        context['leaves'] = user_leaves
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
        
from django.shortcuts import render, redirect
from .models import Lead
from .forms import LeadForm

# View to display the list of leads
def lead_list_alt(request):
    leads = Lead.objects.all()
    return render(request, 'lead_list_alt.html', {'leads': leads})

# View to create a new lead
def lead_create_alt(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alternate_leads_list')
    else:
        form = LeadForm()
    return render(request, 'lead_form_alt.html', {'form': form})

def lead_detail_alt(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'lead_detail_alt.html', {'lead': lead})

def lead_edit_alt(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('alternate_leads_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'lead_form_alt.html', {'form': form, 'lead': lead})

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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def task_edit_alt(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tl_task_edit.html', {'form': form})


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
            return redirect('tl_assigned_task_list')
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



from .models import Attendance, Leave, Break
from .forms import AttendanceForm, LeaveRequestForm

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def mark_attendance(request):
    date = timezone.now().date()  # Get today's date

    # Check if the user is on leave today
    leave_today = Leave.objects.filter(user=request.user, start_date__lte=date, end_date__gte=date, status="Approved").exists()
    if leave_today:
        # Inform the user that they cannot mark attendance as they are on leave
        messages.warning(request, "You are on leave today. Attendance marking is disabled.")
        return redirect('dashboard')

    # Try to get the attendance for the current day
    attendance = Attendance.objects.filter(user=request.user, date=date).first()

    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            if attendance:
                # If attendance exists, update the existing record
                attendance.login_time = form.cleaned_data['login_time']
                attendance.logout_time = form.cleaned_data['logout_time']
                attendance.status = 'Present'  # Set to present as attendance is being marked
                attendance.save()
            else:
                # If no attendance exists, create a new record
                attendance = Attendance(user=request.user, date=date,
                                        login_time=form.cleaned_data['login_time'],
                                        logout_time=form.cleaned_data['logout_time'],
                                        status='Present')
                attendance.save()

            return redirect('dashboard')  # Redirect to the dashboard
    else:
        # If the attendance exists, pre-fill the form with existing data for editing
        if attendance:
            form = AttendanceForm(initial={
                'login_time': attendance.login_time,
                'logout_time': attendance.logout_time
            })
        else:
            form = AttendanceForm()  # Empty form for a new attendance entry

    return render(request, 'mark_attendance.html', {'form': form})


@login_required
def leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()

            return redirect('leave_request_history')  # Redirect to the dashboard
    else:
        form = LeaveRequestForm()

    return render(request, 'leave_request.html', {'form': form})




# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BreakForm

@login_required
def mark_break(request):
    if request.method == 'POST':
        form = BreakForm(request.POST)
        if form.is_valid():
            # Save the break for the logged-in user
            break_instance = form.save(commit=False)
            break_instance.user = request.user
            break_instance.save()
            return redirect('dashboard')  # Redirect to the break list page after saving
    else:
        form = BreakForm()

    return render(request, 'mark_break.html', {'form': form})

@login_required
def break_list(request):
    # Fetch all breaks for the currently logged-in user
    breaks = Break.objects.filter(user=request.user)
    
    # Pass the breaks to the template
    return render(request, 'break_list.html', {'breaks': breaks})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Leave

@login_required
def leave_requests(request):
    # Fetch all leave requests, if the user is an admin or the user themselves
    if request.user.is_staff:
        leave_requests = Leave.objects.all()  # Admin can see all requests
    else:
        leave_requests = Leave.objects.filter(user=request.user)  # Users can see their own requests

    return render(request, 'leave_requests.html', {'leave_requests': leave_requests})


from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    if not request.user.is_staff:
        messages.error(request, "You do not have permission to approve or disapprove leave requests.")
        return redirect('leave_requests')

    if leave.status == 'Pending':  # Ensure that the leave is still pending
        leave.status = 'Approved'
        leave.save()

        # Mark attendance as 'On Leave' for each date in the leave period
        for single_date in [leave.start_date + timezone.timedelta(days=i) for i in range((leave.end_date - leave.start_date).days + 1)]:
            attendance, created = Attendance.objects.get_or_create(user=leave.user, date=single_date)
            attendance.status = 'On Leave'
            attendance.save()

        messages.success(request, f"Leave request from {leave.user.username} approved.")
    else:
        messages.warning(request, f"Leave request from {leave.user.username} is already {leave.status.lower()}.")

    return redirect('leave_requests')


@login_required
def disapprove_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    if not request.user.is_staff:
        messages.error(request, "You do not have permission to approve or disapprove leave requests.")
        return redirect('leave_requests')

    if leave.status == 'Pending':  # Ensure that the leave is still pending
        leave.status = 'Disapproved'
        leave.save()

        # Reset attendance for each date in the leave period to 'Absent' or other default status
        for single_date in [leave.start_date + timezone.timedelta(days=i) for i in range((leave.end_date - leave.start_date).days + 1)]:
            attendance = Attendance.objects.filter(user=leave.user, date=single_date).first()
            if attendance:
                attendance.status = 'Absent'  # Or other default status
                attendance.save()

        messages.success(request, f"Leave request from {leave.user.username} disapproved.")
    else:
        messages.warning(request, f"Leave request from {leave.user.username} is already {leave.status.lower()}.")

    return redirect('leave_requests')


from django.shortcuts import render
from .models import Attendance
from django.utils import timezone

def attendance_on_date(request):
    # Get the date from the query parameter; default to today if not provided
    date_str = request.GET.get('date')
    if date_str:
        try:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()  # Fallback to today if date parsing fails
    else:
        date = timezone.now().date()

    # Retrieve attendance records for the specified date
    attendance_records = Attendance.objects.filter(date=date)

    # Pass the attendance records and date to the template
    context = {
        'attendance_records': attendance_records,
        'date': date,
    }
    return render(request, 'attendance_on_date.html', context)


from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Attendance
from datetime import timedelta

User = get_user_model()

def get_monthly_report(request):
    # Get current year and month
    current_year = timezone.now().year
    current_month = timezone.now().month

    # Get all possible years and months for the dropdown
    years = [current_year, current_year - 1, current_year + 1]
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    # Get selected parameters from the request or use current date as default
    year = int(request.GET.get('year', current_year))  # Convert year to integer
    month = int(request.GET.get('month', current_month))  # Convert month to integer
    start_date_str = request.GET.get('start_date', f'{year}-{month:02d}-01')
    end_date_str = request.GET.get('end_date', f'{year}-{month:02d}-05')

    # Convert the start and end dates to datetime objects
    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')

    # Define the departments with team lead status to exclude
    excluded_departments = [
        'teamlead_development',
        'teamlead_content_moderators',
        'teamlead_sales_team',
        'teamlead_customer_support'
    ]

    # Filter users to exclude superusers and those in excluded team lead departments
    users = User.objects.exclude(
        is_superuser=True
    ).exclude(
        department__in=excluded_departments
    ).distinct()

    monthly_report = []

    # For each user, calculate the number of Present, On Leave, and Absent days
    for user in users:
        attendance_stats = Attendance.calculate_monthly_status_count(user, year, month)
        monthly_report.append({
            'user': user,
            'present_days': attendance_stats['present_days'],
            'on_leave_days': attendance_stats['on_leave_days'],
            'absent_days': attendance_stats['absent_days'],
        })

    context = {
        'monthly_report': monthly_report,
        'year': year,
        'month': month,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'years': years,
        'months': months,
        'month_name': months[month - 1][1]
    }

    return render(request, 'monthly_report.html', context)

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required
def assigned_task_list(request):
    user_tasks = TLTasks.objects.filter(assigned_to=request.user.username)  # Filters tasks where assigned_to matches the username
    return render(request, 'assigned_tasks.html', {'user_tasks': user_tasks})


def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')
        task = get_object_or_404(TLTasks, id=task_id, assigned_to=request.user.username)
        task.status = new_status
        task.save()
        messages.success(request, 'Task status updated successfully.')
    return redirect('assigned_task_list')

from django.shortcuts import render
from .models import Attendance

def attendance_history(request):
    user_attendance = Attendance.objects.filter(user=request.user)  
    return render(request, 'attendance_history.html', {'attendance': user_attendance})

from django.shortcuts import render
from .models import Leave

def leave_request_history(request):
    
    user_leaves = Leave.objects.filter(user=request.user)  
    return render(request, 'leave_request_history.html', {'leaves': user_leaves})
