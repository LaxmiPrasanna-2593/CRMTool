from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import User  # Ensure you import your custom User model

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        department = request.POST.get('department')

        # Validate inputs
        if not username or not email or not password1 or not password2 or not department:
            messages.error(request, "All fields are required.")
            return render(request, 'signup.html')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already associated with an account.")
            return render(request, 'signup.html')

        # Create and save the user
        user = User(
            username=username,
            email=email,
            password=make_password(password1),  # Encrypt and store in password field
            plain_password=password1,  # Store plain password
            department=department
        )
        user.save()

        messages.success(request, "User created successfully! You can now log in.")
        return redirect('signup')  # Redirect to login page after successful signup

    return render(request, 'signup.html', {
        'department_choices': User.DEPARTMENT_CHOICES
    })

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('dashboard')  # Redirect to a protected page (home/dashboard)
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


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

from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
@login_required
def custom_logout_view(request):
    # Log out the user
    logout(request)

    

    # Setting cache control headers to prevent cached pages
    response = HttpResponseRedirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    
    return redirect(reverse('login'))


from django.shortcuts import render, redirect
from .forms import EmployeeForm, TLTaskStatusForm
@login_required
def employee_form_view(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_success')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


@login_required
def employee_success_view(request):
    return render(request, 'employee_sucess.html')  # Render the success template


from django.shortcuts import render, get_object_or_404
from .models import Employee
from django.urls import reverse
@login_required
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
@login_required
# View to show details of a specific employee
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_detail.html', {'employee': employee})
@login_required
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
 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lead
from .forms import LeadForm
from django.contrib.auth.decorators import login_required
@login_required
# View to display the list of leads
def lead_list(request):
    leads = Lead.objects.all()[::-1]
    return render(request, 'lead_list.html', {'leads': leads})

# View to create a new lead
@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)  # Don't save yet, we want to add the user
            lead.created_by = request.user  # Set the logged-in user
            lead.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'lead_form.html', {'form': form})
@login_required
# View to display the lead details
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'lead_detail.html', {'lead': lead})

# View to edit an existing lead
@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            # Only change 'created_by' if it's not already set (optional)
            lead = form.save(commit=False)
            if not lead.created_by:
                lead.created_by = request.user  # Ensure the logged-in user is set
            lead.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'lead_form.html', {'form': form, 'lead': lead})

# View to display the list of leads for an alternative view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Lead

@login_required
def lead_list_alt(request):
    user = request.user  # Get the logged-in user
    
    # Check if the user belongs to the "teamlead_sales_team" department
    if user.department == 'teamlead_sales_team':  # Assuming 'department' is a field on the User model
        # If the user is a team lead, show all leads
        leads = Lead.objects.all()[::-1]
    else:
        # Otherwise, show only the leads created by the user
        leads = Lead.objects.filter(created_by=user)
    
    return render(request, 'lead_list_alt.html', {'leads': leads})


# View to create a new lead for an alternative view
@login_required
def lead_create_alt(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user  # Set the logged-in user
            lead.save()
            return redirect('alternate_leads_list')
    else:
        form = LeadForm()
    return render(request, 'lead_form_alt.html', {'form': form})
@login_required
# View to display the lead details for an alternative view
def lead_detail_alt(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'lead_detail_alt.html', {'lead': lead})

# View to edit an existing lead for an alternative view
@login_required
def lead_edit_alt(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            # Only change 'created_by' if it's not already set (optional)
            lead = form.save(commit=False)
            if not lead.created_by:
                lead.created_by = request.user  # Ensure the logged-in user is set
            lead.save()
            return redirect('alternate_leads_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'lead_form_alt.html', {'form': form, 'lead': lead})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
@login_required
# View to list all tasks
def task_list(request):
    tasks = Task.objects.all()[::-1]
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
@login_required
def tl_task_list(request):
    tasks = TLTasks.objects.all()[::-1]
    return render(request, 'tl_task_list.html', {'tasks': tasks})
@login_required
def tl_task_create(request):
    if request.method == 'POST':
        form = TLTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tl_assigned_task_list')
    else:
        form = TLTaskForm()
    return render(request, 'tl_task_form.html', {'form': form, 'action': 'Create'})
@login_required
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
@login_required
def admin_task_list_view(request):
    tasks = TLTasks.objects.all()[::-1]  # Fetch all tasks from the database
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
@login_required
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
@login_required
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

@login_required
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
@login_required
def attendance_history(request):
    user_attendance = Attendance.objects.filter(user=request.user)  
    return render(request, 'attendance_history.html', {'attendance': user_attendance})

from django.shortcuts import render
from .models import Leave
@login_required
def leave_request_history(request):
    
    user_leaves = Leave.objects.filter(user=request.user)  
    return render(request, 'leave_request_history.html', {'leaves': user_leaves})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, DailyUpdateTaskForm
from .forms import DailyUpdateTaskForm, ProjectForm
from django.db.models import Count

# views.py

from django.shortcuts import render, redirect
from .forms import FormDailyUpdateTaskForm
from django.contrib.auth.decorators import login_required

@login_required
def submit_daily_task(request):
    if request.method == 'POST':
        form = FormDailyUpdateTaskForm(request.POST, user=request.user)  # Pass the logged-in user here
        if form.is_valid():
            form.save()
            return redirect('daily_update_task_list')  # Redirect to some page after saving the task
    else:
        form = FormDailyUpdateTaskForm(user=request.user)  # Pass the logged-in user on GET request

    return render(request, 'submit_daily_task.html', {'form': form})


from .forms import DailyUpdateTaskForm 
# Edit Task (Employees can edit their tasks)
@login_required
def edit_daily_task(request, task_id):
    task = DailyUpdateTaskForm.objects.get(id=task_id)
    if request.method == 'POST':
        form = FormDailyUpdateTaskForm(request.POST, instance=task,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('employee_task_report_on_date')  # Redirect to report after editing
    else:
        form = FormDailyUpdateTaskForm(instance=task,user=request.user)
    
    return render(request, 'edit_daily_task.html', {'form': form, 'task': task})

# Add Project (Admin/Managers can create new projects)
@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'add_project.html', {'form': form})

# Edit Project (Admin/Managers can edit existing projects)
@login_required
def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'edit_project.html', {'form': form, 'project': project})

# Report on the Number of Employees per Project
@login_required
def employees_per_project(request):
    project_employee_count = Project.objects.annotate(employee_count=Count('dailyupdatetaskform__employee', distinct=True))
    
    return render(request, 'employees_per_project.html', {'project_employee_count': project_employee_count})


from django.db.models import Count
from django.shortcuts import render
from .models import DailyUpdateTaskForm

@login_required
def employee_days_worked(request):
    # Query to count distinct work days (dates) per employee and project
    employee_workdays = DailyUpdateTaskForm.objects.values('employee', 'project') \
        .annotate(work_days=Count('date', distinct=True))  # Count distinct dates
    
    # You might want to also include employee and project names to make the data more user-friendly
    for entry in employee_workdays:
        entry['employee_name'] = User.objects.get(id=entry['employee']).username
        entry['project_name'] = Project.objects.get(id=entry['project']).name

    return render(request, 'employee_days_worked.html', {'employee_workdays': employee_workdays})


# Report on Employee Tasks on a Given Date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import DailyUpdateTaskForm, Project

@login_required
def employee_task_report_on_date(request):
    date_str = request.GET.get('date')
    project_id = request.GET.get('project')
    message = ""  # Default message
    
    selected_date = None
    selected_project = None
    
    # Handle date filtering
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None
            message = "Invalid date format. Please use YYYY-MM-DD."
    else:
        message = "No date selected."

    # Handle project filtering (if project ID is provided)
    if project_id:
        try:
            selected_project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            selected_project = None
            message = "Project not found."
    else:
        selected_project = None
    
    # Filter tasks by selected date and project
    tasks_on_date = DailyUpdateTaskForm.objects.all().select_related('employee', 'project')

    if selected_date:
        tasks_on_date = tasks_on_date.filter(date=selected_date)
    if selected_project:
        tasks_on_date = tasks_on_date.filter(project=selected_project)

    return render(request, 'employee_task_report_on_date.html', {
        'tasks_on_date': tasks_on_date,
        'date': selected_date,
        'message': message,
        'projects': Project.objects.all(),  # To show projects in the dropdown
        'selected_project': selected_project
    })


from .models import DailyUpdateTaskForm 
@login_required
def daily_update_task_list(request):
    if request.user.is_superuser:
        # If the user is a superuser, show all tasks
        tasks = DailyUpdateTaskForm.objects.all()[::-1]
    else:
        # For regular users, show only their own tasks
        tasks = DailyUpdateTaskForm.objects.filter(employee=request.user)[::-1]

    return render(request, 'daily_update_task_list.html', {'tasks': tasks})

from .models import Project


@login_required
def project_list(request):
    if request.user.is_superuser:
        # If the user is a superuser, show all projects
        projects = Project.objects.all()[::-1]
    else:
        # For regular users, you can apply additional filters if needed
        projects = Project.objects.all()[::-1]  # Example: Show all projects for regular users

    return render(request, 'project_list.html', {'projects': projects})


from django.db.models import Count
from django.shortcuts import render
from .models import Lead
@login_required
def lead_status_summary(request):
    # Query to count leads grouped by status and created_by
    leads_summary = (
        Lead.objects.values('created_by__username', 'status')  # Group by created_by and status
        .annotate(count=Count('lead_id'))  # Use lead_id instead of id
        .order_by('created_by__username', 'status')  # Optional: Sort by username and status
    )

    # Restructure data for better display
    structured_data = {}
    for entry in leads_summary:
        created_by = entry['created_by__username'] or 'Unassigned'  # Handle null users
        status = entry['status']
        count = entry['count']
        
        if created_by not in structured_data:
            structured_data[created_by] = {'New': 0, 'Contacted': 0, 'Qualified': 0, 'Closed': 0}
        structured_data[created_by][status] = count

    context = {
        'leads_summary': structured_data,
    }
    return render(request, 'leads_summary.html', context)


from datetime import datetime
import re
from django.shortcuts import render
from .models import Employee, User, DailyUpdateTaskForm
@login_required
def user_details_with_projects(request):
    # Fetch all employees
    employees = Employee.objects.all()

    # List to store user details with associated projects
    user_details = []

    # Function to parse experience string
    def parse_experience(experience_str):
        years = 0
        months = 0
        if experience_str:
            # Use regex to extract years and months from the string
            match = re.match(r'(\d+)\s*years?\s*(\d+)\s*months?', experience_str)
            if match:
                years = int(match.group(1))  # Extract years
                months = int(match.group(2))  # Extract months
        return years, months

    # Loop through each employee to fetch details and calculate total experience
    for employee in employees:
        try:
            # Find a User whose email matches the employee's work_mail
            user = User.objects.get(email=employee.work_email)
        except User.DoesNotExist:
            # If no user matches, skip this employee
            continue

        # Fetch DailyUpdateTaskForm entries for the found user
        daily_update_tasks = DailyUpdateTaskForm.objects.filter(employee=user)

        # Extract associated project names from the tasks
        projects = set(task.project.name for task in daily_update_tasks)

        # Parse the previous experience from the employee data
        previous_experience_years, previous_experience_months = parse_experience(employee.previous_Total_work_experience)
        
        # Convert previous experience to total years
        previous_experience_in_years = previous_experience_years * 12 + previous_experience_months  # Total months

        # Get the date of joining
        date_of_joining = employee.date_of_joining

        # If date_of_joining is a datetime object, we need to convert it to date or make both datetime
        if isinstance(date_of_joining, datetime):
            joining_date = date_of_joining.date()  # Convert datetime to date
        else:
            joining_date = date_of_joining

        # Calculate the current experience (difference between now and date_of_joining)
        today = datetime.now().date()
        current_experience_months = (today.year - joining_date.year) * 12 + today.month - joining_date.month

        # Calculate total experience in months
        total_experience_months = previous_experience_in_years + current_experience_months

        # Calculate years and months from total months
        total_experience_years = total_experience_months // 12
        remaining_months = total_experience_months % 12

        # Prepare the total experience string in "X years Y months" format
        total_experience = f"{total_experience_years} years {remaining_months} months"

        # Prepare data for the context
        user_data = {
            'employee': employee,
            'user': user,
            'projects': projects,
            'total_experience': total_experience,
        }
        user_details.append(user_data)

    # Pass the aggregated data to the template
    return render(request, 'user_details.html', {'user_details': user_details})

from django.shortcuts import get_object_or_404
@login_required
def view_employee_portfolio(request, employee_id):
    # Fetch the employee object
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Fetch user details
    try:
        user = User.objects.get(email=employee.work_email)
    except User.DoesNotExist:
        user = None

    # Fetch projects
    daily_update_tasks = DailyUpdateTaskForm.objects.filter(employee=user)
    projects = set(task.project.name for task in daily_update_tasks)

    # Prepare data for the context
    context = {
        'employee': employee,
        'user': user,
        'projects': projects,
    }

    return render(request, 'portfolio.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from EmployeeDashboard.models import User
from django.contrib.auth.decorators import user_passes_test

# Custom decorator to check if the user is a superuser
def superuser_required(view_func):
    return user_passes_test(lambda user: user.is_superuser)(view_func)

@superuser_required
def user_list(request):
    # Fetch all users
    users = User.objects.all().exclude(is_superuser=True)  # Exclude superusers
    department_choices = User.DEPARTMENT_CHOICES  # Fetch department choices

    # Pass the superuser status and department choices to the template
    return render(request, 'user_list.html', {
        'users': users,
        'is_superuser': request.user.is_superuser,
        'department_choices': department_choices
    })

@superuser_required
def delete_user(request, user_id):
    # Fetch the user to delete
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('user_list')  # Redirect to user list after deletion


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Client
from .forms import ClientForm

# Check if the user is a superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# List all clients
@superuser_required
def client_list(request):
    clients = Client.objects.all()[::-1]
    return render(request, 'client_list.html', {'clients': clients})

# Create a new client
@superuser_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client created successfully!")
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client_form.html', {'form': form})

# Edit an existing client
@superuser_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, client_id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully!")
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_form.html', {'form': form, 'client': client})

# Delete a client
@superuser_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, client_id=client_id)
    client.delete()
    messages.success(request, "Client deleted successfully!")
    return redirect('client_list')



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


from django.shortcuts import render, get_object_or_404, redirect
from .forms import AssetForm
from .models import Asset

# Create Asset (Only superusers)
def create_asset(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page if not a superuser
    
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')  # Redirect to asset list after creation
    else:
        form = AssetForm()
    
    return render(request, 'asset_form.html', {'form': form})

# Update Asset (Only superusers)
def update_asset(request, pk):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page if not a superuser
    
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')  # Redirect to asset list after update
    else:
        form = AssetForm(instance=asset)
    
    return render(request, 'asset_form.html', {'form': form})

# Delete Asset (Only superusers)
def delete_asset(request, pk):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page if not a superuser
    
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')  # Redirect to asset list after deletion
    
    return render(request, 'asset_confirm_delete.html', {'asset': asset})

# List Assets (Optionally restrict to superusers)
def asset_list(request):
    if not request.user.is_superuser:
        return redirect('permission_denied')  # Redirect to permission denied page if not a superuser
    
    assets = Asset.objects.all()[::-1]
    return render(request, 'asset_list.html', {'assets': assets})

# Permission Denied (for non-superusers)
def permission_denied(request):
    return render(request, 'permission_denied.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Intern
from .forms import InternForm

@login_required
def intern_list(request):
    interns = Intern.objects.all()  # Fetch all interns
    return render(request, 'intern_list.html', {'interns': interns})

@login_required
def intern_detail(request, pk):
    intern = get_object_or_404(Intern, pk=pk)  # Fetch intern by pk
    return render(request, 'intern_detail.html', {'intern': intern})

@login_required
def intern_create(request):
    if request.method == 'POST':
        form = InternForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save new intern to the database
            return redirect('intern_list')  # Redirect to the intern list after successful save
    else:
        form = InternForm()  # Empty form for GET request
    return render(request, 'intern_form.html', {'form': form})

@login_required
def intern_update(request, pk):
    intern = get_object_or_404(Intern, pk=pk)  # Fetch intern by pk
    if request.method == 'POST':
        form = InternForm(request.POST, request.FILES, instance=intern)  # Fill form with existing intern data
        if form.is_valid():
            form.save()  # Save updated data to the database
            return redirect('intern_detail', pk=intern.pk)  # Redirect to intern detail page after save
    else:
        form = InternForm(instance=intern)  # Populate form with existing intern data for GET request
    return render(request, 'intern_form.html', {'form': form})
