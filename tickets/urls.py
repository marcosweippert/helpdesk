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

    path('forgot_password/', views.forgot_password_view, name='forgot_password'),

    path('read-nfe/', views.read_nfe, name='read_nfe'),


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


    path('companies/', views.company_list, name='company_list'),
    path('companies/<int:company_id>/', views.company_detail, name='company_detail'),
    path('companies/create/', views.company_create, name='company_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('configuration', views.configuration_view, name='configuration'),
    path('companies/<int:company_id>/add_deliverable/', views.add_deliverable_view, name='add_deliverable'),


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


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

