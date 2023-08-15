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


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email do usuário deve ser definido')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário deve ter is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    # Outros campos de usuário

    # Configura o manager personalizado
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


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