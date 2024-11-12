"""
URL configuration for CRMTool project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from EmployeeDashboard.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup_view, name='signup'),
    path('', login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'), 
    path('dashboard/', dashboard_view, name='dashboard'),
    path('employee_form/', employee_form_view, name='employee_form'),
    path('employee_success/', employee_success_view, name='employee_success'), 
    path('employees/', employee_list, name='employee_list'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', edit_employee, name='edit_employee'),
    path('alternate_leads_list/', lead_list_alt, name='alternate_leads_list'),
    path('lead_create_alt/', lead_create_alt, name='lead_create_alt'),
    path('lead_detail_alt/<int:pk>/', lead_detail_alt, name='lead_detail_alt'),
    path('lead_edit_alt/<int:pk>/', lead_edit_alt, name='lead_edit_alt'),
    path('leads/', lead_list, name='lead_list'),
    path('lead_create/', lead_create, name='lead_create'),
    path('lead_detail/<int:pk>/', lead_detail, name='lead_detail'),
    path('lead_edit/<int:pk>/', lead_edit, name='lead_edit'),
    path('task_list/', task_list, name='task_list'),  
    path('task_create/', task_create, name='task_create'),  
    path('task_edit/<int:pk>/', task_edit, name='task_edit'), 
    path('tl_task_list/', tl_task_list, name='tl_task_list'),
    path('tl_task_create/', tl_task_create, name='tl_task_create'),
    path('tl_task_edit/<int:task_id>/', tl_task_edit, name='tl_task_edit'), 
    path('admin_task_list/', admin_task_list_view, name='admin_task_list'),
    path('tl_assigned_task_list/', tlassigned_task_list_view, name='tl_assigned_task_list'),
    path('task/<int:pk>/edit_alt/', task_edit_alt, name='task_edit_alt'),
    path('mark-attendance/', mark_attendance, name='mark_attendance'),
    path('leave-request/', leave_request, name='leave_request'),
    path('approve-leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('mark-break/', mark_break, name='mark_break'), 
    path('break-list/', break_list, name='break_list'),
    path('leave-requests/', leave_requests, name='leave_requests'),
    path('approve_leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('disapprove_leave/<int:leave_id>/', disapprove_leave, name='disapprove_leave'),
    path('attendance/', attendance_on_date, name='attendance_on_date'),
    path('attendance/report/',get_monthly_report, name='monthly_report'),
    path('assigned_task_list/',assigned_task_list, name='assigned_task_list'),
    path('update-task-status/', update_task_status, name='update_task_status'),
    path('attendance-history/', attendance_history, name='attendance_history'),
    path('leave-request-history/', leave_request_history, name='leave_request_history'),
    path('submit-dailytask/', submit_daily_task, name='submit_daily_task'),
    path('edit_daily_task/<int:task_id>/', edit_daily_task, name='edit_daily_task'),
    path('daily_update_task_list/', daily_update_task_list, name='daily_update_task_list'),
    path('add-project/', add_project, name='add_project'),
    path('edit-project/<int:project_id>/', edit_project, name='edit_project'),
    path('employees-per-project/', employees_per_project, name='employees_per_project'),
    path('employee-days-worked/', employee_days_worked, name='employee_days_worked'),
    path('employee-task-report-on-date/', employee_task_report_on_date, name='employee_task_report_on_date'),
    path('projects/', project_list, name='project_list'),



] 
# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)