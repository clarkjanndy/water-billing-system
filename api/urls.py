from django.urls import path

from .views import analytics_views 


urlpatterns = [
    #analytics
    path('consumption/<int:id>', analytics_views.consumption_get, name="consumption_get"), 
    path('consumption-history/<int:id>', analytics_views.consumption_history_get, name="consumption_histogram_get"), 

    path('bills-unpaid/<int:id>', analytics_views.bills_unpaid_get, name="bills_unpaid_get"),
    path('bills-paid-vs-unpaid/<int:id>', analytics_views.bills_paid_vs_unpaid_get, name="bills_paid_vs_unpaid_get"),  
]
    
