from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Ticket, Company, DeliveryCalendar, Workorder
from .forms import UserForm, TicketForm, CompanyForm, WorkorderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta, date, time
from django.utils import timezone
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Comment
from .forms import CommentForm
from django.shortcuts import redirect
from .models import Ticket
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket
from .forms import ChangeAssignedToForm, DeliveryCalendarForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Ticket
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Ticket
from .forms import TicketForm
from .models import Company, CustomUser, DeliveryCalendar
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
import os
import uuid
from django.http import HttpResponse
from django.conf import settings

def get_greeting(request):
    now = datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        greeting = "Bom dia"
    elif 12 <= hour < 18:
        greeting = "Boa tarde"
    else:
        greeting = "Boa noite"

    # Check if the user is authenticated and has a name field
    if request.user.is_authenticated and hasattr(request.user, 'name'):
        user_name = request.user.name
        return f"{greeting}, {user_name}!"
    else:
        return greeting
    
@login_required
def home(request):
    # Exemplo de mensagem de boas-vindas
    welcome_message = get_greeting(request)
    analyst_tickets = Ticket.objects.filter(status='New').values('assigned_to').annotate(total=Count('id'))
    date_tickets = Ticket.objects.filter(status='New').values('created_at__date').annotate(total=Count('id'))
    companies = Company.objects.all()
    users = CustomUser.objects.all()

    context = {
        'companies': companies,
        'users': users,
        'welcome_message': welcome_message,
        'analyst_tickets': analyst_tickets,
        'date_tickets': date_tickets,
    }
    # Renderiza o template 'home.html' passando a mensagem de boas-vindas como contexto
    return render(request, 'geral/home.html', context)

@login_required
def configuration_view(request):
    # Verifica se o usuário autenticado é um superusuário
    if not request.user.is_superuser:
        # Se não for, redireciona para a página inicial ou exibe uma mensagem de erro.
        # Por exemplo, redirecionar para a página de tickets (caso exista):
        return redirect('ticket_list')  # Certifique-se de ajustar o nome da URL de acordo com a sua aplicação

    # Se o usuário for um superusuário, renderize a página de configuração
    return render(request, 'geral/configuration.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to the URL name of your home page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user/login.html')

def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('user_list')
        else:
            print(form.errors)
            # Aqui vamos incluir a mensagem de erro no contexto
            context = {
                'form': form,
                'error_message': 'Erro ao criar usuário. Verifique os campos e tente novamente.',
            }
            return render(request, 'user/user_form.html', context)
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'user/user_form.html', context)

def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})




def ticket_list(request):
    tickets = Ticket.objects.annotate(comments_count=Count('comments'))
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    users = CustomUser.objects.all()
    other_users = users.exclude(pk=request.user.id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        change_assigned_form = ChangeAssignedToForm(request.POST)

        if form.is_valid() and change_assigned_form.is_valid():
            comment = form.cleaned_data['comment']
            ticket.comments.create(author=request.user, body=comment, ticket=ticket)

            selected_users = request.POST.getlist('to')
            for user_id in selected_users:
                user = CustomUser.objects.get(pk=user_id)
                if user != request.user:
                    send_mail_to_user(user, ticket, comment)

            return redirect('ticket_detail', ticket_id=ticket_id)
    else:
        form = CommentForm()
        change_assigned_form = ChangeAssignedToForm()

    context = {
        'ticket': ticket,
        'users': users,
        'other_users': other_users,
        'form': form,
        'change_assigned_form': change_assigned_form,
    }
    return render(request, 'tickets/ticket_detail.html', context)

def send_mail_to_user(user, ticket, comment):
    subject = f"Notificação sobre o ticket {ticket.id}"
    from_email = 'seu_email@exemplo.com'  # Substitua pelo seu e-mail
    recipient_list = [user.email]
    
    # Carregar o template de e-mail e substituir os campos dinâmicos pelo valor correto
    context = {
        'user': user,  # Aqui utilizamos o objeto CustomUser
        'ticket': ticket,
        'comment': comment,
    }
    html_message = render_to_string('tickets/email/comment_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)



def sla_calculation(created_at, priority):
    if priority == 'Low':
        prazo = 48
    elif priority == 'Medium':
        prazo = 24
    elif priority == 'High':
        prazo = 4
    elif priority == 'Urgent':
        prazo = 2
    elif priority == 'Scheduled':
        prazo = 72
    else:
        raise ValueError('Invalid Priority.')

    # Adiciona o prazo em horas à data de criação
    sla_date = created_at + timedelta(hours=prazo)

    # Verifica se a data limite cai em um sábado ou domingo
    while sla_date.weekday() >= 5:
        # Se cair em um fim de semana, ajusta para o início da próxima semana (segunda-feira)
        sla_date += timedelta(days=(7 - sla_date.weekday()))

    # Define o horário de início e fim do expediente
    start_time = time(9, 0, 0)
    end_time = time(18, 0, 0)

    # Verifica se a data limite está fora do horário de trabalho
    if sla_date.time() < start_time:
        sla_date = datetime.combine(sla_date.date(), start_time)
    elif sla_date.time() > end_time:
        sla_date = datetime.combine(sla_date.date() + timedelta(days=1), start_time)

    return sla_date


#Função original de criação de ticket (individual)
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user

            # Verifica se o campo company foi preenchido no formulário
            if 'company' in form.cleaned_data and form.cleaned_data['company']:
                ticket.company = form.cleaned_data['company']

            # Calcular data de criação do ticket
            ticket.created_at = make_aware(datetime.now())

            # Calcular data limite (SLA) com base na prioridade selecionada
            ticket.sla_date = sla_calculation(ticket.created_at, ticket.priority)

            ticket.save()
            print("Ticket created successfully!")
            return redirect('ticket_detail', ticket_id=ticket.id)
        else:
            print("Form is not valid:", form.errors)
    else:
        form = TicketForm()

    companies = Company.objects.all()
    users = CustomUser.objects.all()

    context = {
        'form': form,
        'companies': companies,
        'users': users,
    }

    return render(request, 'tickets/ticket_form.html', context)




# Signal to create tickets when a DeliveryCalendar is added
@receiver(post_save, sender=DeliveryCalendar)
def create_tickets(sender, instance, created, **kwargs):
    if created:
        # Mapeamento das atividades para os títulos
        activity_titles = {
            'Changes': 'Payroll Changes',
            'Payroll Preview': 'Payroll Preview',
            'Payroll Approval': 'Payroll Approval',
            'Net Salaries': 'Net Salaries',
            'Taxes': 'Taxes',
            'Accounting': 'Accounting and Provisions',
            'Next Month Vacations': 'Next Month Vacations',
            'eSocial Delivery': 'eSocial Delivery',
        }

        cam = instance.cam
        analyst = instance.analyst
        ticket_sla_date = instance.month_date

        if instance.pay_period == 'Advance':
            # Cria as atividades para pay_period igual a 'Advance'
            activity_titles = {
            'Changes': 'Payroll Changes',
            'Payroll Preview': 'Payroll Preview',
            'Payroll Approval': 'Payroll Approval',
            'Net Salaries': 'Net Salaries',
            }
        
        for activity, title in activity_titles.items():
            Ticket.objects.create(
                title=title,
                description=f'This is an automatic ticket for {activity} activity',
                priority='Medium',
                assigned_to=analyst,
                created_by=cam,
                company=instance.client,
                department='Operation',
                type=activity,
                sla_date=getattr(instance, f'{activity}_date', ticket_sla_date),
            )

from datetime import timedelta
#nessa função é para criar um ticket automaticamente quando um ticket do tipo "termination" é criado e solicitar ao usuario que tire os extratos de FGTS
@receiver(post_save, sender=Ticket)
def create_tickets(sender, instance, created, **kwargs):
    if created and instance.type == 'Termination':
    
        # Mapeamento das atividades para os títulos
        activity_titles = {
            'FGTS': f'FGTS Statement Request from Ticket #{instance.id}',
        }
        cam = instance.created_by
        analyst = instance.assigned_to
        ticket_sla_date = instance.sla_date - timedelta(days=1)  # Subtrair um dia do sla_date
        
        for activity, title in activity_titles.items():
            Ticket.objects.create(
                title=title,
                description=f'This is an automatic ticket for {activity} activity. Please access https://conectividadesocialv2.caixa.gov.br/sicns/ and request for detailed FGTS balance statement for termination calculation.',
                priority='Medium',
                assigned_to=analyst,
                created_by=cam,
                company=instance.company,
                department='Operation',
                type=activity,
                sla_date=getattr(instance, f'{activity}_date', ticket_sla_date),
            )

#aqui a função deve ser cria um ticket a partir de alteração de status do ticket de Vacation para 'closed', criar um ticket para o CAM enviar os entregaveis ao cliente.
@receiver(post_save, sender=Ticket)
def create_tickets(sender, instance, created, **kwargs):
    if not created and instance.type == 'Vacation' and instance.status == 'Closed':
        # Mapeamento das atividades para os títulos
        activity_titles = {
            'Vacation': 'Vacation Activity Completed',
        }
        cam = instance.assigned_to
        analyst = instance.created_by
        ticket_sla_date = instance.closed_at  # Usar a data de conclusão do ticket anterior
        
        for activity, title in activity_titles.items():
            Ticket.objects.create(
                title=title,
                description='The Vacation activity has been completed. Please send the deliverables to the client.',
                priority='Urgent',
                assigned_to=cam,
                created_by=analyst,
                company=instance.company,
                department='Services',
                type=activity,
                sla_date=ticket_sla_date,
            )

def ticket_list_all_closed(request):
    tickets = Ticket.objects.filter(status='Closed').annotate(comments_count=Count('comments'))

    return render(request, 'tickets/ticket_list_closed.html', {'tickets': tickets})

def ticket_list_all_open(request):
    tickets = Ticket.objects.exclude(status='Closed').annotate(comments_count=Count('comments'))
    return render(request, 'tickets/ticket_list_all_open.html', {'tickets': tickets})

def ticket_list_my_open(request):
    user = request.user
    tickets = Ticket.objects.filter(assigned_to=user).exclude(status='Closed').annotate(comments_count=Count('comments'))

    return render(request, 'tickets/ticket_list_my_open.html', {'tickets': tickets})

def ticket_list_my_closed(request):
    # Filtra os tickets em aberto do usuário logado
    user = request.user
    tickets = Ticket.objects.filter(assigned_to=user).filter(status='Closed').annotate(comments_count=Count('comments'))

    return render(request, 'tickets/ticket_list_my_closed.html', {'tickets': tickets})

def open_tickets_report_xlsx(request):
    open_tickets = Ticket.objects.exclude(status='Closed')

    # Dicionário de cores para cada valor de prioridade
    priority_colors = {
        'low': '008000',    # Verde
        'medium': 'FFFF00', # Amarelo
        'high': 'FFA500',   # Laranja
        'urgent': 'FF0000', # Vermelho
        'scheduled': '0000FF', # Azul
    }


    # Cria um novo arquivo do Excel
    workbook = Workbook()
    worksheet = workbook.active

    # Define os títulos das colunas
    worksheet['A1'] = 'ID'
    worksheet['B1'] = 'Company'
    worksheet['C1'] = 'Partner'
    worksheet['D1'] = 'Title'
    worksheet['E1'] = 'Requester'
    worksheet['F1'] = 'Owner'
    worksheet['G1'] = 'Created Date'
    worksheet['H1'] = 'SLA Date'
    worksheet['I1'] = 'Priority'
    worksheet['J1'] = 'Link'

    # Define o alinhamento do texto como centralizado
    for column in worksheet.columns:
        for cell in column:
            cell.alignment = Alignment(horizontal='center')

    # Preenche os dados dos tickets abertos no relatório
    row_index = 2
    for ticket in open_tickets:
        worksheet.cell(row=row_index, column=1, value=ticket.id)
        worksheet.cell(row=row_index, column=2, value=ticket.company.abreviation if ticket.company and hasattr(ticket.company, 'name') else '')
        worksheet.cell(row=row_index, column=3, value=ticket.company.partner)
        worksheet.cell(row=row_index, column=4, value=ticket.title)
        worksheet.cell(row=row_index, column=5, value=ticket.created_by.first_name)
        worksheet.cell(row=row_index, column=6, value=ticket.assigned_to.first_name)
        worksheet.cell(row=row_index, column=7, value=ticket.created_at.replace(tzinfo=None))
        worksheet.cell(row=row_index, column=8, value=ticket.sla_date.replace(tzinfo=None) if ticket.sla_date else None)
        worksheet.cell(row=row_index, column=9, value=ticket.priority)
        worksheet.cell(row=row_index, column=10, value=ticket.link)

        # Aplica a formatação condicional na coluna de prioridade
        priority = ticket.priority.lower()
        color = priority_colors.get(priority, 'FFFFFF')  # Branco se a prioridade não estiver mapeada
        cell = worksheet.cell(row=row_index, column=9)
        fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        cell.fill = fill

        # Verifica se a data SLA é igual à data de hoje e aplica a cor verde
        sla_date = ticket.sla_date.date() if ticket.sla_date else None
        if sla_date == date.today():
            cell.fill = PatternFill(start_color='008000', end_color='008000', fill_type='solid')  # Cor verde

        row_index += 1

    unique_id = str(uuid.uuid4())[:5]  # Obtém os primeiros 5 caracteres do UUID
    
    # Define o nome do arquivo do relatório com o identificador único
    report_filename = f'Open_Tickets_{unique_id}.xlsx'

    # Define o caminho completo onde o arquivo será salvo
    report_path = os.path.join(settings.MEDIA_ROOT, 'reports', report_filename)

    # Salva o arquivo do Excel
    workbook.save(report_path)

    # Envia o arquivo como resposta para o navegador
    with open(report_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + report_filename
        return response



def is_admin(user):
    return user.is_superuser

@csrf_exempt
def change_ticket_status(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        new_status = request.POST.get('new_status')

        try:
            ticket = Ticket.objects.get(pk=ticket_id)

            if ticket.status == 'Closed' and new_status != 'Closed':
                # If the ticket is closed, only superusers can change it to another status
                if not request.user.is_superuser:
                    return JsonResponse({'success': False, 'error': 'Only superusers can change the status of a closed ticket.'})
                ticket.closed_by = None  # Remove the user who closed the ticket

            if ticket.status != 'Closed' and new_status == 'Closed':
                ticket.closed_by = request.user  # Save the instance of the logged-in user

            ticket.status = new_status
            ticket.save()
            return JsonResponse({'success': True})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ticket not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def change_ticket_assigned_to(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ChangeAssignedToForm(request.POST)
        if form.is_valid():
            assigned_to = form.cleaned_data['assigned_to']
            ticket.assigned_to = assigned_to
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = ChangeAssignedToForm()

    return render(request, 'tickets/change_assigned_to.html', {'form': form})

def ticket_close(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        # Lógica para tratamento de ticket não encontrado (opcional)
        return redirect('ticket_list')  # Redireciona de volta para a lista de tickets

    # Verifica se o ticket já está fechado
    if ticket.status == 'closed':
        # Lógica para tratamento de ticket já fechado (opcional)
        return redirect('ticket_list')  # Redireciona de volta para a lista de tickets

    # Atualiza os campos de fechamento do ticket
    ticket.closed_at = now()
    ticket.closed_by = request.user
    ticket.status = 'Closed'
    ticket.save()

    # Redireciona de volta para a lista de tickets após o fechamento
    return redirect('ticket_list_all_open')



def company_list(request):

    companies = Company.objects.all()
    return render(request, 'company/company_list.html', {'companies': companies})

@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    
    # Recupera os usuários para preencher os campos de CAM, CAM Backup, Analyst e Analyst Backup
    users = CustomUser.objects.all()

    return render(request, 'company/company_form.html', {'form': form, 'users': users})

from django.shortcuts import render, redirect
from .models import Company, Deliverable
from .forms import DeliverableForm

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    deliverable = Deliverable.objects.all()

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.company = company
            deliverable.save()
            return redirect('company_detail', company_id=company_id)
    else:
        form = DeliverableForm()

    return render(request, 'company/company_detail.html', {'company': company, 'form': form, 'deliverables': deliverable})


def add_deliverable_view(request, company_id):
    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.company = company
            deliverable.save()
            return redirect('company_detail', company_id=company_id)
    else:
        form = DeliverableForm()

    return render(request, 'calendar/add_deliverable.html', {'form': form, 'company': company})







def delivery_calendar_create(request):
    if request.method == 'POST':
        form = DeliveryCalendarForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # Print form data to debug
            form.save()
            return redirect('delivery_calendar_list')
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = DeliveryCalendarForm()
    
    return render(request, 'calendar/delivery_calendar_form.html', {'form': form})

def delivery_calendar_detail(request, pk):
    calendar = get_object_or_404(DeliveryCalendar, pk=pk)
    return render(request, 'calendar/delivery_calendar_detail.html', {'calendar': calendar})

def delivery_calendar_update(request, pk):
    calendar = get_object_or_404(DeliveryCalendar, pk=pk)
    if request.method == 'POST':
        form = DeliveryCalendarForm(request.POST, instance=calendar)
        if form.is_valid():
            form.save()
            return redirect('delivery_calendar_detail', pk=calendar.pk)
    else:
        form = DeliveryCalendarForm(instance=calendar)
    return render(request, 'calendar/delivery_calendar_form.html', {'form': form, 'calendar': calendar})

def delivery_calendar_list(request):
    calendars = DeliveryCalendar.objects.all()
    return render(request, 'calendar/delivery_calendar_list.html', {'calendars': calendars})

def delivery_calendar_delete(request, pk):
    calendar = get_object_or_404(DeliveryCalendar, pk=pk)
    if request.method == 'POST':
        calendar.delete()
        return redirect('delivery_calendar_list')
    return render(request, 'calendar/delivery_calendar_confirm_delete.html', {'calendar': calendar})



@login_required
def create_work_order(request):
    if request.method == 'POST':
        form = WorkorderForm(request.POST)
        if form.is_valid():
            work_order = form.save(commit=False)
            work_order.created_by = request.user
            work_order.save()
            return redirect('analyze_work_order')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = WorkorderForm()

    companies = Company.objects.all()
    users = CustomUser.objects.all()

    context = {
        'form': form,
        'companies': companies,
        'users': users,
    }

    return render(request, 'workorder/create_workorder.html', context)

def analyze_work_order(request):
    if request.method == 'POST':
        workorder_id = request.POST.get('workorder_id')
        cam_approval = request.POST.get('cam_approval')
        workorder = Workorder.objects.get(id=workorder_id)
        
        if cam_approval == 'Approve':
            workorder.status = 'In Progress'
            workorder.cam_approval = 'Approved'
            workorder.save()
            return redirect('execute_work_order')
        elif cam_approval == 'Reprove':
            workorder.status = 'Rework'
            workorder.cam_approval = 'Reproved'
            workorder.assigned_to = workorder.created_by  # Return to the analyst who created the work order
            workorder.save()
            return redirect('rework_work_order')

    workorders = Workorder.objects.filter(status='New')

    context = {
        'workorders': workorders,
        'users': CustomUser.objects.all(),  # Pass the list of users for Assigned To field
    }

    return render(request, 'workorder/analyze_workorder.html', context)


def approve_work_order(request):
    # Listar as Work Orders aprovadas pelo Setor de Serviços
    if request.method == 'POST':
        # Processar a aprovação da Work Order
        # Redirecionar para a próxima etapa ou rework se necessário
        return redirect('execute_work_order')
    return render(request, 'workorder/approve_workorder.html', {'workorders': Workorder.objects.filter(status='Waiting on us')})

def execute_work_order(request):
    # Listar as Work Orders aprovadas pelo Cliente
    if request.method == 'POST':
        # Processar a execução da Work Order
        # Redirecionar para a próxima etapa ou rework se necessário
        return redirect('closed')
    return render(request, 'workorder/execute_workorder.html', {'workorders': Workorder.objects.filter(status='Waiting on contact')})

def rework_work_order(request):
    # Listar as Work Orders que precisam de retrabalho
    if request.method == 'POST':
        # Processar o retrabalho da Work Order
        # Redirecionar para a próxima etapa
        return redirect('analyze_work_order')
    return render(request, 'workorder/rework_workorder.html', {'workorders': Workorder.objects.filter(status='Cancelled')})

def work_order_dashboard(request):
    workorders = Workorder.objects.all()
    return render(request, 'workorder/workorder_dashboard.html', {'workorders': workorders})