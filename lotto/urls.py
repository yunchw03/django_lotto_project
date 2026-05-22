from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.buy_page, name='buy_page'),
    
    path('buy-auto/<int:round_id>/', views.buy_auto, name='buy_auto'),
    
    path('buy-manual/<int:round_id>/', views.buy_manual, name='buy_manual'),
]