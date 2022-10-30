from django.urls import path

from .views import page_views
from .views import admin_views
from .views import consumer_views
from .views import baranggay_views
from .views import reading_views
from .views import collectible_views

urlpatterns = [
    path('', page_views.landing_page, name="landing_page"),  
    path('login', page_views.login, name="login"),
    path('change-password', page_views.change_password, name="change_password"),

    path('admin', admin_views.admin, name="admin-panel"),

    path('consumers', consumer_views.index, name="consumers"),
    path('consumers/add', consumer_views.add_consumer, name="add_consumer"),
    path('consumers/<int:id>', consumer_views.view_consumer, name="view_consumer"),
    path('consumers/<int:id>/edit', consumer_views.edit_consumer, name="edit_consumer"),
    path('consumers/<int:id>/readings', consumer_views.view_consumer_readings, name="view_consumer_readings"),
    path('consumers/<int:id>/bills', consumer_views.view_consumer_bills, name="view_consumer_bills"),
    
    path('baranggays', baranggay_views.index, name="baranggays"),
    path('baranggays/add', baranggay_views.add_baranggay, name="add_baranggay"),
    path('baranggays/<int:id>', baranggay_views.view_baranggay, name="view_baranggay"),
    path('baranggays/<int:id>/edit', baranggay_views.edit_baranggay, name="edit_baranggay"), 
    
    path('readings/add', reading_views.add_reading, name="add_reading"),
    path('readings/<int:id>/edit', reading_views.edit_reading, name="edit_reading"), 

    path('bills/<int:id>/', collectible_views.view_collectible, name="view_collectible"),

    path('print/bills/<int:id>', collectible_views.print_collectible, name="print_collectible"),     
    
    path('logout', page_views.logout, name="logout"),   
]
    
