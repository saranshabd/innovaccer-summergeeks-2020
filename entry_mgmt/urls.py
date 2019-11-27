from django.urls import path
from . import views


urlpatterns = [
    path('check_in/', views.check_in),
    path('check_out/', views.check_out),
]
