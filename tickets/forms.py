# forms.py (aplicativo de usuários)

from django import forms
from .models import CustomUser, Company, Ticket, Comment, DeliveryCalendar, Deliverable, Workorder

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'is_superuser', 'is_cam', 'is_analyst', 'is_manager']


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