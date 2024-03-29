from base.views import notification_views
from django.urls import path

from .views import page_views, admin_views, consumer_views, baranggay_views, reading_views, collectible_views, report_views, projection_views, settings_views

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
    path('admin/projections', admin_views.projections, name="projections"),
    path('admin/reports', admin_views.reports, name="reports"),
    
    path('admin/settings', admin_views.settings, name="settings"),
    path('admin/settings/add', settings_views.add_setting, name="settings"),
    path('admin/settings/edit', settings_views.edit_reading, name="settings"),
    
    
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
    
    path('projections/add/', projection_views.add, name="add_pojection"),
    path('projections/update/', projection_views.update, name="update_pojection"),
    path('projections/<int:id>/delete', projection_views.delete, name="update_pojection"),
   
    
    # printable reports
    path('admin/print-monthly-report/<int:id>/', report_views.print_monthly_report, name="print_monthly_report"),
    path('admin/print-barangay-report/<int:id>/', report_views.print_barangay_report, name="print_barangay_report"),
         
    path('logout/', page_views.logout, name="logout"),   
]
    
