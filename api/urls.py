from django.urls import path

from .views import analytics_views, validation_views, action_views


urlpatterns = [
    #validation
    path('validate-password', validation_views.validate_password, name="check_password"),
    path('validate-username', validation_views.validate_username, name="validate_username"),
    path('validate-meter', validation_views.validate_meter, name="validate_meter"),
    path('validate-billing-month', validation_views.validate_billing_month, name="validate_billing_month"),
    path('validate-projection-month', validation_views.validate_projection_month, name="validate_projection_month"),

    #analytics
    path('consumer-count', analytics_views.consumer_count, name="consumer_count"),
    path('baranggay-count', analytics_views.barangay_count, name="barangay_count"),
    path('transaction-history-count', analytics_views.transaction_history_count, name="transaction_history_count"),
    path('admin-count', analytics_views.admin_count, name="admin_count"),
    path('notifications/<int:id>', analytics_views.notification_unseen_get, name="notification_unseen_get"),
    path('password-reset-request-count', analytics_views.password_reset_request_count, name="password_reset_request_count"),

    path('consumption', analytics_views.consumption_all, name="consumption_all"),
    path('consumption-by-month', analytics_views.consumption_all_by_month, name="consumption_all_by_month"),
    path('consumption/<int:id>', analytics_views.consumption_get, name="consumption_get"), 
    path('consumption-histogram', analytics_views.consumption_history_all, name="consumption_histogram_all"),
    path('consumption-histogram/<int:id>', analytics_views.consumption_history_get, name="consumption_histogram_get"), 
    path('consumption-pie-chart', analytics_views.consumption_pie_chart, name="consumption_pie_chart"), 

    path('bills-paid', analytics_views.bills_paid_all, name="bills_paid_all"),
    path('bills-paid-by-month', analytics_views.bills_paid_all_by_month, name="bills_paid_all_by_month"),
    path('bills-unpaid', analytics_views.bills_unpaid_all, name="bills_unpaid_all"),
    path('bills-unpaid/<int:id>', analytics_views.bills_unpaid_get, name="bills_unpaid_get"),
    path('bills-paid-vs-unpaid/<int:id>', analytics_views.bills_paid_vs_unpaid_get, name="bills_paid_vs_unpaid_get"), 
    
    
    path('collection-histogram', analytics_views.collection_histogram, name="collection_histogram"), 
    path('collection-radial', analytics_views.collection_radial, name="collection_radial"),  
       

    #actions
    path('action/make-admin', action_views.make_admin, name="make_admin"), 
    path('action/read-notification', action_views.read_notification, name="read_notification"),
    path('action/notification-mark-all-as-read', action_views.notification_mark_all_as_read, name="notification_mark_all_as_read"),
    path('action/notification-delete-all', action_views.notification_delete_all, name="notification_delete_all"),  
]  

    
