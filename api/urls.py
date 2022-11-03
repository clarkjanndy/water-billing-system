from django.urls import path

from .views import analytics_views, validation_views, action_views


urlpatterns = [
    #validation
    path('validate-password', validation_views.validate_password, name="check_password"),
    path('validate-meter', validation_views.validate_meter, name="validate_meter"),
    path('validate-billing-month', validation_views.validate_billing_month, name="validate_billing_month"),

    #analytics
    path('consumer-count', analytics_views.consumer_count, name="consumer_count"),
    path('baranggay-count', analytics_views.barangay_count, name="barangay_count"),
    path('transaction-history-count', analytics_views.transaction_history_count, name="transaction_history_count"),
    path('admin-count', analytics_views.admin_count, name="admin_count"),
    path('notifications/<int:id>', analytics_views.notification_unseen_get, name="notification_unseen_get"),

    path('consumption', analytics_views.consumption_all, name="consumption_all"),
    path('consumption/<int:id>', analytics_views.consumption_get, name="consumption_get"), 
    path('consumption-history/<int:id>', analytics_views.consumption_history_get, name="consumption_histogram_get"), 

    path('bills-paid', analytics_views.bills_paid_all, name="bills_paid_all"),
    path('bills-unpaid', analytics_views.bills_unpaid_all, name="bills_unpaid_all"),
    path('bills-unpaid/<int:id>', analytics_views.bills_unpaid_get, name="bills_unpaid_get"),
    path('bills-paid-vs-unpaid/<int:id>', analytics_views.bills_paid_vs_unpaid_get, name="bills_paid_vs_unpaid_get"),  

    #actions
    path('action/make-admin', action_views.make_admin, name="make_admin"), 
    path('action/read-notification', action_views.read_notification, name="read_notification"),
    path('action/notification-mark-all-as-read', action_views.notification_mark_all_as_read, name="notification_mark_all_as_read"),
    path('action/notification-delete-all', action_views.notification_delete_all, name="notification_delete_all"),  
]  

    
