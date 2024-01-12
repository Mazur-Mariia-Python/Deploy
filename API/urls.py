from django.urls import path
from . import views

urlpatterns = [
    path('get_gifts/', views.api_load_response_data),
]
