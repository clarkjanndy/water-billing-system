from django.urls import path

from .views import analytics_views, validation_views, action_views


urlpatterns = [
    #validation
    path('validate-password', validation_views.validate_password, name="check_password"),
    path('validate-meter', validation_views.validate_meter, name="validate_meter"),
    path('validate-billing-month', validation_views.validate_billing_month, name="validate_billing_month"),

    #analytics
    path('consumption/<int:id>', analytics_views.consumption_get, name="consumption_get"), 
    path('consumption-history/<int:id>', analytics_views.consumption_history_get, name="consumption_histogram_get"), 

    path('bills-unpaid/<int:id>', analytics_views.bills_unpaid_get, name="bills_unpaid_get"),
    path('bills-paid-vs-unpaid/<int:id>', analytics_views.bills_paid_vs_unpaid_get, name="bills_paid_vs_unpaid_get"),  

    #actions
    path('action/make-admin', action_views.make_admin, name="make_admin"),  
]
    
