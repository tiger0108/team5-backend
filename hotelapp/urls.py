from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.get_hotels, name='get_hotels'),
    # path('', views.show_hotels, name='show_hotels'),
]
