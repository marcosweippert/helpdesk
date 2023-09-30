# forms.py (aplicativo de usuários)

from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser', 'is_cam', 'is_analyst', 'is_manager', 'is_driver']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'assigned_to', 'sla_date', 'company', 'attachment', 'type', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].empty_label = "Não atribuído"

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'



class ChangeAssignedToForm(forms.Form):
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Digite seu comentário aqui...', 'required': True}))
    to = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Comment
        fields = ('author', 'body', 'to')
 

class DeliveryCalendarForm(forms.ModelForm):
    class Meta:
        model = DeliveryCalendar
        fields = ['pay_period', 'cam', 'analyst', 'client', 'month_date', 'changes_date', 'payroll_preview_date', 'approval_date', 'net_salaries_date', 'taxes_date', 'accounting_date', 'next_month_vacations_date', 'esocial_delivery_date']

class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ['payroll_report', 'naming_convention', 'delivery_format', 'delivery_type', 'frequency', 'delivery_date']

class WorkorderForm(forms.ModelForm):
    class Meta:
        model = Workorder
        fields = ['company', 'department', 'type', 'hours', 'priority', 'description', 'assigned_to']

class ManualInvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label=_("Email"),
    )
class DriverRegistrationForm(forms.ModelForm):
    is_driver = forms.BooleanField(initial=True, widget=forms.HiddenInput())  # Campo para definir que é um motorista
    bank_id = forms.ModelChoiceField(queryset=Bank.objects.all(), empty_label="Select a Bank")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'cpf', 'cnpj', 'bank_id', 'branch', 'account_type', 'account_number', 'account_digit', 'is_driver']

class AuthCpfForm(forms.ModelForm):
    class Meta:
        model = AuthCpf
        fields = ['cpf', 'cnpj']

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'code']



class ChangesUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Selecione o arquivo Excel',
        widget=forms.ClearableFileInput(attrs={'accept': '.xlsx, .xls'})
    )
    company = forms.ModelChoiceField(queryset=Company.objects.all(), label='Selecione a Empresa')
