from base.views import notification_views
from django.urls import path

from .views import page_views
from .views import admin_views
from .views import consumer_views
from .views import baranggay_views
from .views import reading_views
from .views import collectible_views
from .views import report_views

urlpatterns = [
    path('', page_views.landing_page, name="landing_page"),  
    path('init', page_views.init, name="initialize"), 
    path('login', page_views.login, name="login"),
    path('change-password', page_views.change_password, name="change_password"),
    path('send-reset-request', page_views.send_reset_request, name="send_reset_request"),

    path('admin/dashboard', admin_views.dashboard, name="dashboard"),
    path('admin/users', admin_views.users, name="users"),
    path('admin/users/<int:id>', admin_views.view_user, name="view-user"),
    path('admin/transaction-history', admin_views.transaction_history, name="transaction-history"),
    path('admin/consumption-histogram', admin_views.consumption_histogram, name="consumption_histogram"),
    path('admin/password-reset-requests', admin_views.password_reset_requests, name="password_reset_requests"),
    path('admin/treasury-and-transactions', admin_views.treasury_and_transactions, name="treasury_and_transactions"),
    path('admin/reports', admin_views.reports, name="reports"),
    
    path('admin/approve-password-reset-request/<int:id>', admin_views.approve_password_reset_request, name="approve_password_reset_request"),
    path('admin/delete-password-reset-request/<int:id>', admin_views.delete_password_reset_request, name="delete_password_reset_request"),
    
    path('consumers', consumer_views.index, name="consumers"),
    path('consumers/add', consumer_views.add_consumer, name="add_consumer"),
    path('consumers/<int:id>', consumer_views.view_consumer, name="view_consumer"),
    path('consumers/<int:id>/edit', consumer_views.edit_consumer, name="edit_consumer"),
    path('consumers/<int:id>/readings', consumer_views.view_consumer_readings, name="view_consumer_readings"),
    path('consumers/<int:id>/bills', consumer_views.view_consumer_bills, name="view_consumer_bills"),

    path('notifications', notification_views.get_notifications, name="get_notifications"),
    path('transaction-history', notification_views.get_transaction_history, name="get_transaction_history"),
    
    path('baranggays', baranggay_views.index, name="baranggays"),
    path('baranggays/add', baranggay_views.add_baranggay, name="add_baranggay"),
    path('baranggays/<int:id>', baranggay_views.view_baranggay, name="view_baranggay"),
    path('baranggays/<int:id>/edit', baranggay_views.edit_baranggay, name="edit_baranggay"), 
    
    path('readings/add', reading_views.add_reading, name="add_reading"),
    path('readings/<int:id>/edit', reading_views.edit_reading, name="edit_reading"), 

    path('bills/<int:id>/', collectible_views.view_collectible, name="view_collectible"),
    path('transact/<int:id>', collectible_views.transact, name="transact"),
    path('transact/complete', collectible_views.transact_complete, name="transact_complete"),
    path('transact/view/<int:id>', collectible_views.transact_view, name="transact_view"),

    path('print/bills/<int:id>', collectible_views.print_collectible, name="print_collectible"),
    path('print/reciept/<int:id>', collectible_views.print_reciept, name="print_reciept"),
    
    # printable reports
    path('report/consumption/', report_views.print_consumption, name="print_consumption"),
         
    path('logout', page_views.logout, name="logout"),   
]
    
