from django import forms
from .models import Employee, Leave, Project, User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
       
        fields = [
            # Personal Information
            'first_name', 'middle_name', 'last_name','profile_picture', 'employee_status','dob', 'place_of_birth', 'father_name',
            'gender', 'marital_status', 'nationality', 'blood_group', 'address', 'city', 'state',
            'zip_code', 'mobile', 'alternate_phone', 'personal_email', 'work_email', 
            'passport_no', 'passport_valid_from', 'passport_valid_upto', 'passport_file_upload',
            'visa_file_upload',

            # PAN Details
            'pan_name', 'pan_number', 'pan_upload_file',

            # Aadhar Details
            'aadhar_name', 'aadhar_number', 'aadhar_file_upload',

            # Provident Fund Information
            'pf_member', 'pf_number', 'pf_withdrawn', 'uan_number', 'uan_confirmed', 'active_visa',

            # Job Information
            'employee_id', 'date_of_joining', 'position', 'department', 'employment_type',
            'reporting_manager', 'job_location', 'work_schedule', 'job_related_documents',

            # Educational Qualifications
            'highest_degree', 'institution_name', 'field_of_study', 'year_of_graduation', 'certifications',

            # Previous Experience
            'previous_company_name', 'previous_job_title', 'previous_work_location', 'previous_exit_date',
            'responsibilities', 'reason_for_leaving',

            # Reference Information
            'reference_1_name', 'reference_1_designation', 'reference_1_company_name', 'reference_1_contact', 'reference_1_email',
            'reference_2_name', 'reference_2_designation', 'reference_2_company_name', 'reference_2_contact', 'reference_2_email',

            # Emergency Contact Information
            'emergency_first_name', 'emergency_middle_name', 'emergency_last_name', 'emergency_relationship',
            'emergency_home_phone', 'emergency_mobile_phone', 'emergency_city', 'emergency_state', 'emergency_zip_code',

            # Bank Information
            'bank_name_on_account', 'bank_account_number', 'bank_name', 'bank_branch_name', 'bank_ifsc_code',
            'bank_branch_address', 'passbook_file_upload',

            # Files Upload for Current Employment
            'offer_letter', 'nda_form', 'btech_memo', 'btech_tc', 'relieving_letter', 'experience_letter', 'payslips',
        ]
        fields = '__all__'
        widgets = {
            # Date fields
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'passport_valid_from': forms.DateInput(attrs={'type': 'date'}),
            'passport_valid_upto': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
            'exit_date': forms.DateInput(attrs={'type': 'date'}),
            'previous_start_date': forms.DateInput(attrs={'type': 'date'}),
            'previous_exit_date': forms.DateInput(attrs={'type': 'date'}),

            # TextInput for smaller fields
            'mobile': forms.TextInput(attrs={'type': 'tel'}),
            'alternate_phone': forms.TextInput(attrs={'type': 'tel'}),
            'personal_email': forms.EmailInput(attrs={'type': 'email'}),
            'work_email': forms.EmailInput(attrs={'type': 'email'}),
            'zip_code': forms.TextInput(attrs={'type': 'text'}),

            # File Input for document fields
            'profile_picture': forms.FileInput(),
            'passport_file_upload': forms.FileInput(),
            'visa_file_upload': forms.FileInput(),
            'pan_upload_file': forms.FileInput(),
            'aadhar_file_upload': forms.FileInput(),
            'job_related_documents': forms.FileInput(),
            'certifications': forms.FileInput(),
            'passbook_file_upload': forms.FileInput(),
            'offer_letter': forms.FileInput(),
            'nda_form': forms.FileInput(),
            'btech_memo': forms.FileInput(),
            'btech_tc': forms.FileInput(),
            'relieving_letter': forms.FileInput(),
            'experience_letter': forms.FileInput(),
            'payslips': forms.FileInput(),

            # Dropdown fields for choice fields
            'gender': forms.Select(),
            'marital_status': forms.Select(),
            'employment_type': forms.Select(),
            'pf_member': forms.Select(),
            'pf_withdrawn': forms.Select(),
            'uan_confirmed': forms.Select(),
            'active_visa': forms.Select(),
            'employee_status':forms.Select(),
        }

from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name', 'email', 'phone_number', 'company_name', 'position',
            'lead_source', 'status', 'interest_level', 'last_contact_date',
            'next_follow_up_date', 'product_interest', 'estimated_deal_value', 'notes',
        ]
        widgets = {
            'last_contact_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'next_follow_up_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }        

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date', 'priority', 'notes']

        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


from .models import TLTasks
class TLTaskForm(forms.ModelForm):
    class Meta:
        model = TLTasks
        fields = ['title', 'description', 'assigned_to', 'assigned_by', 'priority', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import TLTasks

class TLTaskStatusForm(forms.ModelForm):
    class Meta:
        model = TLTasks
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }




from django import forms
from .models import Attendance, Break

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['login_time', 'logout_time', 'date']
        widgets = {
            'login_time': forms.TimeInput(attrs={'type': 'time'}),
            'logout_time': forms.TimeInput(attrs={'type': 'time'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BreakForm(forms.ModelForm):
    class Meta:
        model = Break
        fields = ['date','break_start_time', 'break_end_time', 'reason']
        widgets = {
            'break_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'break_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date','end_date', 'leave_type', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    leave_type = forms.ChoiceField(choices=[('Sick', 'Sick'), ('Vacation', 'Vacation'), ('Casual', 'Casual')], required=True)
    reason = forms.CharField(widget=forms.Textarea, required=True)



# forms.py

from django import forms
from .models import DailyUpdateTaskForm, User

class FormDailyUpdateTaskForm(forms.ModelForm):
    class Meta:
        model = DailyUpdateTaskForm
        fields = ['task_description', 'date', 'employee', 'project', 'task_status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'task_status': forms.Select(choices=DailyUpdateTaskForm.TASK_STATUS_CHOICES),  # Dropdown for task_status
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop 'user' from kwargs if passed from view
        super(FormDailyUpdateTaskForm, self).__init__(*args, **kwargs)
        
        if user:
            # Set the 'employee' field to the current logged-in user
            self.fields['employee'].initial = user
            # Optionally, you can also restrict the queryset to the logged-in user
            self.fields['employee'].queryset = User.objects.filter(id=user.id)
        else:
            # Handle case if no user is passed (shouldn't happen in this case)
            self.fields['employee'].queryset = User.objects.none()



class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }



from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone_number', 'status', 'project_name', 
                  'services_utilized', 'deal_cost', 'contract_start_date', 
                  'contract_end_date', 'payment_status', 'notes', 
                  'acquisition_source', 'account_manager']
    contract_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False  # You can make this optional if you want
    )
    
    contract_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False  # You can make this optional if you want
    )


from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name', 'category', 'description', 'purchase_cost', 'purchase_date',
            'purchased_from', 'contact_details', 'warranty_expiration',
            'serial_number', 'location', 'maintenance_date', 'quantity',
            'repair_history', 'last_repair_date', 'repair_cost', 'repair_vendor', 'repair_notes'
        ]

    # Defining widgets for each field
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asset Name'}),
    )
    purchase_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    warranty_expiration = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        input_formats=['%Y-%m-%d']
    )
    maintenance_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        input_formats=['%Y-%m-%d']
    )
    last_repair_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        input_formats=['%Y-%m-%d']
    )
    purchase_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        min_value=0.01
    )
    repair_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        required=False,
        min_value=0.00
    )
    category = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=Asset.CATEGORY_CHOICES
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the asset...'}),
        required=False
    )
    purchased_from = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor or Company'}),
        required=False
    )
    contact_details = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact details'}),
        required=False
    )
    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
        required=False
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location of the asset'}),
        required=False
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        initial=1,
        min_value=1
    )
    repair_history = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Details of past repairs'}),
        required=False
    )
    repair_vendor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Repair Vendor'}),
        required=False
    )
    repair_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes about repairs'}),
        required=False
    )


from django import forms
from .models import Intern

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = '__all__'
        widgets = {
            # Basic Information
            'full_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter email address'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter contact number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),

            # Internship Details
            'role': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter role'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter department'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'mode_of_work': forms.Select(attrs={
                'class': 'form-control'
            }),
            'supervisor': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter supervisor name'
            }),

            # Educational Details
            'university': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter university name'
            }),
            'degree': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter degree'
            }),
            'year_of_study': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter year of study'
            }),
            'major': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter major'
            }),

            # Compensation and Benefits
            'stipend': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter stipend amount'
            }),
            'other_benefits': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter details of other benefits'
            }),

            # Performance and Evaluation
            'tasks_assigned': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter tasks assigned'
            }),
            'key_projects': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter key projects'
            }),
            'performance_reviews': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter performance reviews'
            }),
            'skills_learned': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter skills learned'
            }),
            'completion_certificate_issued': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'overall_rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter overall rating (1-10)'
            }),

            # Administrative Details
            'intern_id': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter intern ID'
            }),
            'joining_letter_issued': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'exit_feedback_collected': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            # Optional Fields
            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter LinkedIn profile URL'
            }),
            'emergency_contact': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter emergency contact details'
            }),
            'hobbies': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Enter hobbies'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
