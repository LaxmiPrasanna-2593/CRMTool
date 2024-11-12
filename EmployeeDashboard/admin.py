from django.contrib import admin
from EmployeeDashboard.models import *
from .models import Task

# Register your models here.
admin.site.register(Employee)
admin.site.register(User)
admin.site.register(Task)
admin.site.register(TLTasks)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(Break)
admin.site.register(DailyUpdateTaskForm)
admin.site.register(Project)
