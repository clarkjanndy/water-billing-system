from django.urls import path

from .views import CustomUserList, CustomUserRetrieveUpdateDestroy


urlpatterns = [
    path('users/', CustomUserList.as_view()),
    path('users/<int:id>', CustomUserRetrieveUpdateDestroy.as_view()),        
]
    
