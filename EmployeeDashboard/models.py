from django.contrib.auth.models import AbstractUser
from django.db import models

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

    def _str_(self):
        return self.username


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
        ('Contract', 'Contract')
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
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    dob = models.DateField(verbose_name="Date of Birth")
    place_of_birth = models.CharField(max_length=100)
    employee_status=models.CharField(max_length=15, choices=EMPLOYEE_STATUS_CHOICES)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    address = models.TextField(verbose_name="Current Address")
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20)
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
    pan_name = models.CharField(max_length=100, verbose_name="Name as on PAN")
    pan_number = models.CharField(max_length=10)
    pan_upload_file = models.FileField(upload_to='pan_docs/', blank=True, null=True)

    # ======================
    # Aadhar Details
    # ======================
    aadhar_name = models.CharField(max_length=100, verbose_name="Name as on Aadhar")
    aadhar_number = models.CharField(max_length=12)
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
    date_of_joining = models.DateField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=15, choices=EMPLOYMENT_TYPE_CHOICES)
    reporting_manager = models.CharField(max_length=100)
    job_location = models.CharField(max_length=100)
    work_schedule = models.CharField(max_length=50)
    job_related_documents = models.FileField(upload_to='job_docs/', blank=True, null=True)

    # ======================
    # Educational Qualifications
    # ======================
    highest_degree = models.CharField(max_length=50)
    institution_name = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=50)
    year_of_graduation = models.IntegerField()
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)

    # ======================
    # Previous Experience
    # ======================
    previous_company_name = models.CharField(max_length=100)
    previous_job_title = models.CharField(max_length=50)
    previous_work_location = models.CharField(max_length=100)
    previous_exit_date = models.DateField()
    responsibilities = models.TextField()
    reason_for_leaving = models.TextField()

    # ======================
    # Reference Information
    # ======================
    reference_1_name = models.CharField(max_length=100)
    reference_1_designation = models.CharField(max_length=50)
    reference_1_company_name = models.CharField(max_length=100)
    reference_1_contact = models.CharField(max_length=20)
    reference_1_email = models.EmailField()

    reference_2_name = models.CharField(max_length=100)
    reference_2_designation = models.CharField(max_length=50)
    reference_2_company_name = models.CharField(max_length=100)
    reference_2_contact = models.CharField(max_length=20)
    reference_2_email = models.EmailField()

    # ======================
    # Emergency Contact Information
    # ======================
    emergency_first_name = models.CharField(max_length=100)
    emergency_middle_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_last_name = models.CharField(max_length=100)
    emergency_relationship = models.CharField(max_length=50)
    emergency_home_phone = models.CharField(max_length=20)
    emergency_mobile_phone = models.CharField(max_length=20)
    emergency_city = models.CharField(max_length=50)
    emergency_state = models.CharField(max_length=50)
    emergency_zip_code = models.CharField(max_length=10)

    # ======================
    # Bank Information
    # ======================
    bank_name_on_account = models.CharField(max_length=100, verbose_name="Name as on Bank Account")
    bank_account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    bank_branch_name = models.CharField(max_length=100)
    bank_ifsc_code = models.CharField(max_length=11)
    bank_branch_address = models.TextField()
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
