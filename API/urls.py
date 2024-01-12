from django.urls import path
from . import views

urlpatterns = [
    path('get_gifts/', views.api_load_response_data),
    path("selected_gifts/", views.selected_gifts_list, name="selected_gifts"),
]
