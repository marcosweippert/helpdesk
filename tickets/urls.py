from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),


    path('read_nfe/', views.read_nfe, name='read_nfe'),
    path('create_manual_invoice/', views.create_manual_invoice, name='create_manual_invoice'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('driver_check', views.driver_check, name='driver_check'),
    path('invoice_finance_approval/', views.invoice_finance_approval, name='invoice_finance_approval'),

    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:ticket_id>/close/', views.ticket_close, name='ticket_close'),
    path('my_open_tickets/', views.ticket_list_my_open, name='ticket_list_my_open'),
    path('my_closed_tickets/', views.ticket_list_my_closed, name='ticket_list_my_closed'),
    path('tickets/<int:ticket_id>/change_assigned_to/', views.change_ticket_assigned_to, name='change_ticket_assigned_to'),
    path('tickets/<int:ticket_id>/change_status/', views.change_ticket_status, name='change_ticket_status'),
    path('closed_tickets/', views.ticket_list_all_closed, name='ticket_list_all_closed'),
    path('open_tickets/', views.ticket_list_all_open, name='ticket_list_all_open'),
    path('open_tickets_report/', views.open_tickets_report_xlsx, name='open_tickets_report_xlsx'),
    path('tickets/delete/', views.delete_tickets, name='delete_tickets'),

    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('companies/create/', views.company_create, name='company_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('configuration', views.configuration_view, name='configuration'),
    path('companies/<int:company_id>/add_deliverable/', views.add_deliverable_view, name='add_deliverable'),
    path('companies/edit/<int:company_id>/', views.company_edit, name='company_edit'),
    path('company/<int:company_id>/delete/', views.company_delete, name='company_delete'),

    path('delivery_calendars/', views.delivery_calendar_list, name='delivery_calendar_list'),
    path('delivery_calendars/create/', views.delivery_calendar_create, name='delivery_calendar_create'),
    path('delivery_calendars/<int:pk>/', views.delivery_calendar_detail, name='delivery_calendar_detail'),
    path('delivery_calendars/<int:pk>/update/', views.delivery_calendar_update, name='delivery_calendar_update'),
    path('delivery_calendars/<int:pk>/delete/', views.delivery_calendar_delete, name='delivery_calendar_delete'),

    path('create_work_order/', views.create_work_order, name='create_work_order'),
    path('analyze_work_order/', views.analyze_work_order, name='analyze_work_order'),
    path('execute_work_order/', views.execute_work_order, name='execute_work_order'),
    path('rework_work_order/', views.rework_work_order, name='rework_work_order'),
    path('work_order_dashboard/', views.work_order_dashboard, name='work_order_dashboard'),
    path('edit_work_order/<int:workorder_id>/', views.edit_work_order, name='edit_work_order'),
    path('report_workorder/', views.report_workorder, name='report_work_order'),
    path('workorder/<int:workorder_id>/', views.details_workorder, name='details_workorder'),

    path('driver_register/', views.driver_registration, name='driver_registration'),
    path('auth_cpf/', views.auth_cpf, name='auth_cpf'),
    path('create_bank/', views.create_bank, name='create_bank'),

    path('changes_upload/', views.changes_upload, name='changes_upload'),
    path('delete_changes/', views.delete_changes, name='delete_changes'),
    path('upload_generate/', views.upload_generate, name='upload_generate'),

    path('pay_elements_upload/', views.pay_elements_upload, name='pay_elements_upload'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

