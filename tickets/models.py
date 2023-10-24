from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import *

class Bank(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email do usuário deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def create_cam(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_cam', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um CAM deve ter is_staff=True.')
        return self.create_user(email, password, **extra_fields)

    def create_analyst(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_analyst', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um Analista deve ter is_staff=True.')
        return self.create_user(email, password, **extra_fields)

    def create_manager(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um Gerente deve ter is_staff=True.')
        return self.create_user(email, password, **extra_fields)

    def create_driver(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_manager', False)
        extra_fields.setdefault('is_driver', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Um Driver deve ter is_staff=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_cam = models.BooleanField('CAM', default=False)
    is_analyst = models.BooleanField('Analyst', default=False)
    is_manager = models.BooleanField('Manager', default=False)
    is_driver = models.BooleanField('Driver', default=False)

    ACCOUNT_TYPES_CHOICES = (
        ('Checking', 'Checking'),
        ('Savings', 'Savings'),
    )
    # Campos específicos para drivers
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.CharField(max_length=6, blank=True, null=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES_CHOICES, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_digit = models.CharField(max_length=2, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

class Drivers(models.Model):
    driver = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='driver_profile', blank=True, null=True)
    ACCOUNT_TYPES_CHOICES = (
        ('Checking', 'Checking'),
        ('Savings', 'Savings'),
    )
    # Campos específicos para drivers
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)
    branch = models.CharField(max_length=6, blank=True, null=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES_CHOICES, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_digit = models.CharField(max_length=2, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return f"Driver-{self.driver.username}"
    
class Invoice(models.Model):
    number = models.CharField(max_length=20)
    series = models.CharField(max_length=10)
    issuance_date = models.DateField()
    exit_date = models.DateField()
    emitter_cnpj = models.CharField(max_length=14)
    emitter_name = models.CharField(max_length=200)
    recipient_cnpj = models.CharField(max_length=14, null=True, blank=True)
    recipient_name = models.CharField(max_length=200, null=True, blank=True)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Finance Approval', 'Finance Approval'),
        ('Operation Approval', 'Operation Approval'),
        ('Paid', 'Paid'),
        ('Driver Check', 'Driver Check'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    approval_comments = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='approved_invoices', null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    finance_approval_comments = models.TextField(blank=True, null=True)
    finance_approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='finance_approved_invoices', null=True, blank=True)
    finance_approval_date = models.DateTimeField(null=True, blank=True)
    sla_date = models.DateField(null=True, blank=True)
    operation_approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='operation_approved_invoices', null=True, blank=True)
    operation_approval_date = models.DateTimeField(null=True, blank=True)
    operation_approval_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Invoice-{self.number}"
    
class ApprovalLog(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    approval_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ApprovalLog-{self.id}"

class Protocol(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    protocol_number = models.CharField(max_length=20, unique=True)

class Company(models.Model):
    name = models.CharField(max_length=100)
    abreviation = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    partner = models.CharField(max_length=100)
    cam = models.ForeignKey(CustomUser, related_name='company_cams', on_delete=models.CASCADE, default='10')
    cam_backup = models.ForeignKey(CustomUser, related_name='company_cams_backup', on_delete=models.CASCADE, default='10')
    analyst = models.ForeignKey(CustomUser, related_name='company_analysts', on_delete=models.CASCADE, default='10',  null=True)
    analyst_backup = models.ForeignKey(CustomUser, related_name='company_analysts_backup', on_delete=models.CASCADE, default='10')
    budget_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.0)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Waiting on contact', 'Waiting on contact'),
        ('Waiting on us', 'Waiting on us'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
    )

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
        ('Scheduled', 'Scheduled'),
    )
    DEPARTMENT_CHOICES = (
        ('Operation', 'Operation'),
        ('Tecnology', 'Tecnology'),
        ('Administration', 'Administration'),
        ('Services', 'Services'),
        ('Accounting', 'Accounting'),
    )
    TYPE_CHOICES = (
        #Operation
        ('Payroll', 'Payroll'),
        ('Vacations', 'Vacations'),
        ('Termination', 'Termination'),
        ('New Hire', 'New Hire'),
        ('Requests', 'Requests'),
        ('Changes', 'Changes'),
        ('Taxes', 'Taxes'),
        ('esocial', 'eSocial'),
        ('Payroll Requests', 'Payroll Requests'),
        ('Sick Leave', 'Sick Leave'),
        ('Paylips Dashboard', 'Paylips Dashboard'),
        ('Payroll Requests', 'Payroll Requests'),
        ('Payroll Support', 'Payroll Support'),
        ('Payrrol Accounting', 'Payroll Accounting'),
        #services
        ('Work Order', 'Work Order'),
        #Tecnology
        ('Customization (IT)', 'Customization(IT)'),
        ('Functionality correction(IT)', 'Functionality correction(IT)'),
        ('Rule Replication(IT)', 'Rule Replication(IT)'),
        ('User support (IT)', 'User support (IT)'),
        #Accounting
        ('Provisions', 'Provisions'),
        ('Accounting Support', 'Accounting Support'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='created_tickets')
    closed_at = models.DateTimeField(null=True, blank=True)
    sla_date = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(Company,null=True, blank=True, on_delete=models.CASCADE)
    link = models.URLField(null=True, blank=True)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True, default='Operation')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, null=True, blank=True)
    closed_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='ticket_close')
    change_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='changed_tickets')
   

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class DeliveryCalendar(models.Model):
    PAY_CHOICES = (
        ('Monthly', 'Monthly'),
        ('Advance', 'Advance'),
)
    DELIVERY_CHOICES = (
        ('Per payroll run', 'Per payroll run'),
        ('Per event', 'Per event'),
)
    
    pay_period = models.CharField(max_length=15, choices=PAY_CHOICES, default='Monthly')
    client = models.ForeignKey('Company', on_delete=models.CASCADE)
    cam = models.ForeignKey(CustomUser, related_name='cam_deliveries', on_delete=models.SET_NULL, null=True, blank=True)
    analyst = models.ForeignKey(CustomUser, related_name='analyst_deliveries', on_delete=models.SET_NULL, null=True, blank=True)
    month_date = models.DateField()
    changes_date = models.DateField(null=True, blank=True)
    payroll_preview_date = models.DateField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    net_salaries_date = models.DateField(null=True, blank=True)
    taxes_date = models.DateField(null=True, blank=True)
    accounting_date = models.DateField(null=True, blank=True)
    next_month_vacations_date = models.DateField(null=True, blank=True)
    esocial_delivery_date = models.DateField(null=True, blank=True)

class Deliverable(models.Model):
    DELIVERY_CHOICES = (
        #Operation
        ('Payroll', 'Payroll'),
        ('Vacations', 'Vacations'),
        ('Termination', 'Termination'),
        ('New Hires', 'New Hires'),
        ('13th Salary', '13th Salary'),
        ('Taxes', 'Taxes'),
        ('Annual Statutary Declarations', 'Annual Statutary Declarations'),
        ('Accounting', 'Accounting'),
    )
    FREQUENCY_CHOICES = (
        #Operation
        ('Monthly', 'Monthly'),
        ('On Demand', 'On Demand'),
        ('Annually', 'Annually'),
    )
    DELIVERYDATE_CHOICES = (
    ('Per event', 'Per event'),
    ('Per payroll run', 'Per payroll run'),
    ) + tuple((str(i), str(i)) for i in range(1, 13))

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    payroll_report = models.CharField(max_length=100)
    naming_convention = models.CharField(max_length=100)
    delivery_format = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=100, choices=DELIVERY_CHOICES, null=True, blank=True)
    frequency = models.CharField(max_length=100, choices=FREQUENCY_CHOICES, null=True, blank=True)
    delivery_date = models.CharField(max_length=20, choices=DELIVERYDATE_CHOICES, null=True, blank=True)


    def __str__(self):
        return f"Deliverables for {self.company.name}"
    
class Workorder(models.Model):
    DEPARTMENT_CHOICES = (
        ('Services', 'Services'),
        ('Accounting', 'Accounting'),
    )
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Waiting on contact', 'Waiting on contact'),
        ('Waiting on us', 'Waiting on us'),
        ('Closed', 'Closed'),
        ('Cancelled', 'Cancelled'),
        ('Approved by CAM', 'Approved by CAM'),
        ('Waiting Analyst', 'Waiting Analyst'),
        ('Approved by Analyst', 'Approved by Analyst'),
        ('Waiting CAM', 'Waiting CAM'),
        ('In Progress', 'In Progress'),
        ('Pending', 'Pending'),
    )
    TYPE_CHOICES = (
        ('Work Order', 'Work Order'),
        ('RSA', 'RSA'),

    )
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
        ('Scheduled', 'Scheduled'),
    )
    APPROVAL_CHOICES = (
        ('Approve', 'Approve'),
        ('Reprove', 'Reprove'),
        ('Approved by CAM', 'Approved by CAM'),
        ('Approved by Analyst', 'Approved by Analyst'),
    )
    BILLING_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),

    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorder')
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='created_workorder')
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, null=True, blank=True, default='Services')
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    cam_approval = models.CharField(max_length=30, choices=APPROVAL_CHOICES, null=True, blank=True)
    analyst_approval = models.CharField(max_length=30, choices=APPROVAL_CHOICES, null=True, blank=True)
    billing = models.CharField(max_length=30, choices=BILLING_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    sla_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    approve_date = models.DateTimeField(null=True, blank=True)
    billing_date = models.DateTimeField(null=True, blank=True)
    complete_date = models.DateTimeField(null=True, blank=True)




    def __str__(self):
        return f"Workorder for {self.company.name}"

class AuthCpf(models.Model):
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)

    def __str__(self):
        return self.cpf
    
class ChangesValidation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Payroll_Name = models.CharField(max_length=50)
    Employee_Name = models.CharField(max_length=50, null=False)
    Employee_ID_Number = models.IntegerField(null=False)
    Pay_Period = models.DateField(blank=True, null=True)
    Payroll_Pay_Element = models.CharField(max_length=50, null=False)
    Transaction_Type = models.CharField(max_length=50, null=False)
    Element_Type = models.CharField(max_length=50, null=False)
    Effective_Date = models.DateField(null=False)
    End_Date = models.DateField(blank=True, null=True)
    Amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    Number = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    Unit_Code = models.CharField(max_length=10, blank=True, null=True)
    Unit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    Rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    Payroll_Effective_Date = models.DateField(blank=True, null=True)
    Termination_Date = models.DateField(blank=True, null=True)
    Comments = models.CharField(max_length=255, blank=True, null=True)
    ICP_EEPR_ID = models.IntegerField(blank=True, null=True)
    ICP_Payroll_PayElement = models.CharField(max_length=50, blank=True, null=True)
    ICP_Pay_Element_Code = models.CharField(max_length=10, blank=True, null=True)