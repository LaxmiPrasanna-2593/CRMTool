from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    DEPARTMENT_CHOICES = [
        ('development', 'Development'),
        ('teamlead_development', 'TeamLead_Development'),
        ('content_moderators', 'Content Moderators'),
        ('teamlead_content_moderators', 'TeamLead_Content Moderators'),
        ('sales_team', 'Sales Team'),
        ('teamlead_sales_team', 'TeamLead_Sales Team'),
        ('customer_support', 'Customer Support Team'),
        ('teamlead_customer_support', 'TeamLead_Customer Support Team'),
    ]
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    plain_password = models.CharField(max_length=255, blank=True, null=True)
    

    def _str_(self):
        return self.username

from datetime import date
from dateutil.relativedelta import relativedelta
class Employee(models.Model):
    # Choices for dropdown fields
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married')
    ]
    EMPLOYMENT_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Intern', 'Intern')
    ]
    EMPLOYEE_STATUS_CHOICES=[
        ('Active','Active'),
        ('InActive','InActive')
    ]
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]

    # ======================
    # Personal Information
    # ======================
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    dob = models.DateField(verbose_name="Date of Birth",blank=True, null=True)
    place_of_birth = models.CharField(max_length=100,blank=True, null=True)
    employee_status=models.CharField(max_length=15, choices=EMPLOYEE_STATUS_CHOICES)
    father_name = models.CharField(max_length=100,blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=50,blank=True, null=True)
    blood_group = models.CharField(max_length=3, blank=True, null=True,)
    address = models.TextField(verbose_name="Current Address",blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    zip_code = models.CharField(max_length=10,blank=True, null=True)
    mobile = models.CharField(max_length=20,blank=True, null=True)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    personal_email = models.EmailField()
    work_email = models.EmailField()
    passport_no = models.CharField(max_length=20, blank=True, null=True)
    passport_valid_from = models.DateField(blank=True, null=True)
    passport_valid_upto = models.DateField(blank=True, null=True)
    passport_file_upload = models.FileField(upload_to='passport_docs/', blank=True, null=True)
    visa_file_upload = models.FileField(upload_to='visa_docs/', blank=True, null=True)

    # ======================
    # PAN Details
    # ======================
    pan_name = models.CharField(max_length=100, verbose_name="Name as on PAN",blank=True, null=True)
    pan_number = models.CharField(max_length=10,blank=True, null=True)
    pan_upload_file = models.FileField(upload_to='pan_docs/', blank=True, null=True)

    # ======================
    # Aadhar Details
    # ======================
    aadhar_name = models.CharField(max_length=100, verbose_name="Name as on Aadhar",blank=True, null=True)
    aadhar_number = models.CharField(max_length=12,blank=True, null=True)
    aadhar_file_upload = models.FileField(upload_to='aadhar_docs/', blank=True, null=True)

    # ======================
    # Provident Fund Information
    # ======================
    pf_member = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', verbose_name="Are you a member of PF?")
    pf_number = models.CharField(max_length=20, blank=True, null=True)
    pf_withdrawn = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No', verbose_name="Have you withdrawn from previous PF account?")
    uan_number = models.CharField(max_length=20, blank=True, null=True)
    uan_confirmed = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')
    active_visa = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='No')

    # ======================
    # Job Information
    # ======================
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_joining = models.DateField(blank=True, null=True)
    exit_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=50,blank=True, null=True)
    department = models.CharField(max_length=50,blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES)
    reporting_manager = models.CharField(max_length=100,blank=True, null=True)
    job_location = models.CharField(max_length=100,blank=True, null=True)
    work_schedule = models.CharField(max_length=50,blank=True, null=True)
    
    skill_set=models.TextField(blank=True, null=True)
    job_related_documents = models.FileField(upload_to='job_docs/', blank=True, null=True)

    # ======================
    # Educational Qualifications
    # ======================
    highest_degree = models.CharField(max_length=50,blank=True, null=True)
    institution_name = models.CharField(max_length=100,blank=True, null=True)
    field_of_study = models.CharField(max_length=50,blank=True, null=True)
    year_of_graduation = models.IntegerField(blank=True, null=True)
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)

    # ======================
    # Previous Experience
    # ======================
    previous_company_name = models.CharField(max_length=100,blank=True, null=True)
    previous_job_title = models.CharField(max_length=50,blank=True, null=True)
    previous_work_location = models.CharField(max_length=100,blank=True, null=True)
    previous_start_date=models.DateField(blank=True, null=True)
    previous_exit_date = models.DateField(blank=True, null=True)
    previous_Total_work_experience=models.CharField(max_length=20,blank=True, null=True,verbose_name="Previous Experience (Enter in this format(2 years 3 months))",)
    previous_projects=models.TextField(blank=True, null=True)
    previous_responsibilities = models.TextField(blank=True, null=True)
    previous_achievements = models.TextField(blank=True, null=True)
    reason_for_leaving = models.TextField(blank=True, null=True)

    # ======================
    # Reference Information
    # ======================
    reference_1_name = models.CharField(max_length=100,blank=True, null=True)
    reference_1_designation = models.CharField(max_length=50,blank=True, null=True)
    reference_1_company_name = models.CharField(max_length=100,blank=True, null=True)
    reference_1_contact = models.CharField(max_length=20,blank=True, null=True)
    reference_1_email = models.EmailField(blank=True, null=True)

    reference_2_name = models.CharField(max_length=100,blank=True, null=True)
    reference_2_designation = models.CharField(max_length=50,blank=True, null=True)
    reference_2_company_name = models.CharField(max_length=100,blank=True, null=True)
    reference_2_contact = models.CharField(max_length=20,blank=True, null=True)
    reference_2_email = models.EmailField(blank=True, null=True)

    # ======================
    # Emergency Contact Information
    # ======================
    emergency_first_name = models.CharField(max_length=100,blank=True, null=True)
    emergency_middle_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_last_name = models.CharField(max_length=100,blank=True, null=True)
    emergency_relationship = models.CharField(max_length=50,blank=True, null=True)
    emergency_home_phone = models.CharField(max_length=20,blank=True, null=True)
    emergency_mobile_phone = models.CharField(max_length=20,blank=True, null=True)
    emergency_city = models.CharField(max_length=50,blank=True, null=True)
    emergency_state = models.CharField(max_length=50,blank=True, null=True)
    emergency_zip_code = models.CharField(max_length=10,blank=True, null=True)

    # ======================
    # Bank Information
    # ======================
    bank_name_on_account = models.CharField(max_length=100, verbose_name="Name as on Bank Account",blank=True, null=True)
    bank_account_number = models.CharField(max_length=20,blank=True, null=True)
    bank_name = models.CharField(max_length=100,blank=True, null=True)
    bank_branch_name = models.CharField(max_length=100,blank=True, null=True)
    bank_ifsc_code = models.CharField(max_length=11,blank=True, null=True)
    bank_branch_address = models.TextField(blank=True, null=True)
    passbook_file_upload = models.FileField(upload_to='passbook_docs/', blank=True, null=True)

    # ======================
    # Files Upload for Current Employment
    # ======================
    offer_letter = models.FileField(upload_to='employee_docs/offer_letters/', blank=True, null=True)
    nda_form = models.FileField(upload_to='employee_docs/nda_forms/', blank=True, null=True)
    btech_memo = models.FileField(upload_to='employee_docs/btech_memo/', blank=True, null=True)
    btech_tc = models.FileField(upload_to='employee_docs/btech_tc/', blank=True, null=True)
    relieving_letter = models.FileField(upload_to='employee_docs/relieving_letters/', blank=True, null=True)
    experience_letter = models.FileField(upload_to='employee_docs/experience_letters/', blank=True, null=True)
    payslips = models.FileField(upload_to='employee_docs/payslips/', blank=True, null=True)  # Allows multiple files upload

    
    
    def _str_(self):
        return f"{self.first_name} {self.last_name}"

class Lead(models.Model):
    lead_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)  
    lead_source = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Closed', 'Closed')
    ])
    interest_level = models.CharField(max_length=50, choices=[
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ], blank=True, null=True)
    last_contact_date = models.DateTimeField(blank=True, null=True)
    next_follow_up_date = models.DateTimeField(blank=True, null=True)
    product_interest = models.CharField(max_length=100, blank=True, null=True)
    estimated_deal_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads_created')

    def _str_(self):
        return f"{self.name} - {self.company_name}"
    
from django.db import models
from django.core.exceptions import ValidationError

class Task(models.Model):
    # Basic Information
    title = models.CharField(max_length=255)  # Task title
    description = models.TextField()  # Detailed description of the task

    # Assigned Role
    ASSIGNED_ROLES = [
        ('Dev_TL', 'Development Team Lead'),
        ('Sales_TL', 'Sales Team Lead'),
        ('Content_TL', 'Content Moderator Team Lead'),
        ('Support_TL', 'Customer Support Team Lead'),
    ]
    
    assigned_to = models.CharField(
        max_length=60,
        choices=ASSIGNED_ROLES,
        default='Dev_TL',
    )  # Dropdown with specified roles

    # Assignment and Status
    created_by = models.CharField(max_length=150)  # Store username instead of ForeignKey
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('On Hold', 'On Hold')
        ],
        default='Pending'
    )  # Task status

    # Dates and Deadlines
    created_at = models.DateTimeField(auto_now_add=True)  # Date task was created
    updated_at = models.DateTimeField(auto_now=True)  # Date task was last updated
    due_date = models.DateTimeField()  # Task due date

    # Priority
    priority = models.CharField(
        max_length=20,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High'),
            ('Urgent', 'Urgent')
        ],
        default='Medium'
    )  # Priority level

    # Additional Notes
    notes = models.TextField(blank=True, null=True)  # Additional notes or comments about the task

    def __str__(self):
        return f"{self.title} - {self.status}"

    def clean(self):
        """Custom validation to ensure 'created_by' is an admin user."""
        if self.created_by and not User.objects.filter(username=self.created_by, is_staff=True).exists():
            raise ValidationError("Created by must be an admin user.")
    
    class Meta:
        ordering = ['due_date', 'priority']




class TLTasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.CharField(max_length=100) 
    assigned_by = models.CharField(max_length=100) 
    priority = models.CharField(max_length=20, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ], default='Pending')

    def __str__(self):
        return f"{self.title} - {self.status} (Assigned to {self.assigned_to})"

from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('On Leave', 'On Leave')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    login_time = models.TimeField(null=True, blank=True)
    logout_time = models.TimeField(null=True, blank=True)
    break_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_working_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')

    def calculate_break_time(self):
        """Calculate the total break time in hours."""
        breaks = Break.objects.filter(user=self.user, date=self.date)
        total_break_seconds = sum(
            (timezone.datetime.combine(timezone.datetime.min, b.break_end_time) -
             timezone.datetime.combine(timezone.datetime.min, b.break_start_time)).total_seconds()
            for b in breaks
        )
        total_break_hours = total_break_seconds / 3600
        self.break_time = Decimal(total_break_hours)
        return self.break_time

    def convert_decimal_to_hours_minutes(self, decimal_value):
        if decimal_value is None:
            return "0:00"
        
        hours = int(decimal_value)
        minutes = int((decimal_value - hours) * 60)
        return f"{hours}:{minutes:02d}"

    def get_break_time_in_hours_minutes(self):
        if self.break_time:
            return self.convert_decimal_to_hours_minutes(self.break_time)
        return "00:00"
    
    def convert_total_working_hours_to_hours_minutes(self):
        if self.total_working_hours:
            return self.convert_decimal_to_hours_minutes(self.total_working_hours)
        return "00:00"
    
    def save(self, *args, **kwargs):
        if self.login_time and self.logout_time:
            work_duration = timezone.datetime.combine(timezone.datetime.min, self.logout_time) - timezone.datetime.combine(timezone.datetime.min, self.login_time)
            total_hours = Decimal(work_duration.total_seconds() / 3600)
            
            self.calculate_break_time()
            
            if self.break_time:
                total_hours -= self.break_time
                
            self.total_working_hours = max(total_hours, Decimal('0.0'))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.convert_decimal_to_hours_minutes(self.total_working_hours)} - {self.status}"
    @classmethod
    def calculate_monthly_status_count(cls, user, year, month):
        # Set the start and end date for the 5th-to-5th month period
        start_date = timezone.datetime(year, month, 5)
        end_date = start_date + timedelta(days=31)
        end_date = timezone.datetime(end_date.year, end_date.month, 5)

        # Filter attendance records for the given user between start and end dates
        attendance_records = cls.objects.filter(user=user, date__gte=start_date.date(), date__lt=end_date.date())

        present_days = 0
        on_leave_days = 0
        absent_days = 0

        # Calculate the number of days Present, On Leave, and Absent
        for record in attendance_records:
            if record.status == 'Present':
                present_days += 1
            elif record.status == 'On Leave':
                on_leave_days += 1
            else:
                absent_days += 1

        return {
            'present_days': present_days,
            'on_leave_days': on_leave_days,
            'absent_days': absent_days,
        }
class Break(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    break_start_time = models.TimeField()
    break_end_time = models.TimeField()
    reason = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_attendance_break_time(self)

    def __str__(self):
        return f"Break for {self.user.username} - {self.break_start_time} to {self.break_end_time}"

@receiver(post_save, sender=Break)
def update_attendance_break_time(instance, **kwargs):
    attendance, created = Attendance.objects.get_or_create(user=instance.user, date=instance.date)
    attendance.save()

class Leave(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Disapproved', 'Disapproved')], default='Pending')
    reason = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.status == 'Approved':
            date_range = [self.start_date + timezone.timedelta(days=i) for i in range((self.end_date - self.start_date).days + 1)]
            for date in date_range:
                attendance, created = Attendance.objects.get_or_create(user=self.user, date=date)
                attendance.status = 'On Leave'
                attendance.save()

    def __str__(self):
        return f"Leave from {self.start_date} to {self.end_date} for {self.user.username}"


# Project Model
class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

# DailyUpdateTaskForm Model with TaskStatus Choices
class DailyUpdateTaskForm(models.Model):
    TASK_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('on_hold', 'On Hold'),
    ]

    task_description = models.TextField()
    date = models.DateField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_status = models.CharField(max_length=30, choices=TASK_STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee.username} - {self.project.name} - {self.date}"
    


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)  # Unique ID for each client
    name = models.CharField(max_length=255)  # Client's name
    email = models.EmailField(unique=True)  # Client's email
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp for when the client is added
    status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Inactive', 'Inactive')],
        default='Active'
    )  # Client status
    
    # Additional fields
    project_name = models.CharField(max_length=255, blank=True)  # Project name
    services_utilized = models.TextField(blank=True)  # Services provided
    deal_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Deal cost
    contract_start_date = models.DateField(blank=True, null=True)  # Contract start date
    contract_end_date = models.DateField(blank=True, null=True)  # Contract end date
    payment_status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Overdue', 'Overdue')],
        default='Pending'
    )  # Payment status
    notes = models.TextField(blank=True)  # Additional notes
    acquisition_source = models.CharField(max_length=255, blank=True)  # How the client was acquired
    account_manager = models.CharField(max_length=255, blank=True)  # Responsible staff member

    def __str__(self):
        return self.name


from django.db import models

class Asset(models.Model):
    CATEGORY_CHOICES = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('license', 'License'),
        ('furniture', 'Furniture'), 
        ('peripherals', 'Peripherals'),  
        ('others','Others'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    purchased_from = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the vendor or company the asset was purchased from.")
    contact_details = models.CharField(max_length=255, blank=True, null=True, help_text="Contact details of the vendor or purchasing owner.")
    warranty_expiration = models.DateField(blank=True, null=True, help_text="Warranty expiration date of the asset.")
    serial_number = models.CharField(max_length=1255, blank=True, null=True, help_text="Unique serial number of the asset.")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Physical location of the asset (e.g., Office Room #).")
    maintenance_date = models.DateField(blank=True, null=True, help_text="Next scheduled maintenance date.")
    quantity = models.PositiveIntegerField(default=1, help_text="Number of units of the asset.")

    def __str__(self):
        return self.name
