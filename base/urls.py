from django.urls import path

from .views import page_views
from .views import admin_views
from .views import consumer_views
from .views import baranggay_views
from .views import reading_views

urlpatterns = [
    path('', page_views.landing_page, name="landing_page"),  
    path('login', page_views.login, name="login"),
    
    path('admin', admin_views.admin, name="admin-panel"),
    path('consumers', consumer_views.index, name="consumers"),
    path('consumers/add', consumer_views.add_consumer, name="add_consumer"),
    path('consumers/<int:id>', consumer_views.view_consumer, name="view_consumer"),
    path('consumers/<int:id>/edit', consumer_views.edit_consumer, name="edit_consumer"),
    path('consumers/<int:id>/readings', consumer_views.view_consumer_readings, name="view_consumer_readings"),
    path('consumers/<int:id>/bills', consumer_views.edit_consumer, name="edit_consumer"),
    
    path('baranggays', baranggay_views.index, name="baranggays"),
    path('baranggays/add', baranggay_views.add_baranggay, name="add_baranggay"),
    path('baranggays/<int:id>', baranggay_views.view_baranggay, name="view_baranggay"),
    path('baranggays/<int:id>/edit', baranggay_views.edit_baranggay, name="edit_baranggay"), 
    
    path('readings/add', reading_views.add_reading, name="add_reading"),      
    
    path('logout', page_views.logout, name="logout"),   
]
    
