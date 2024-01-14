from django.urls import path
from . import views


urlpatterns = [
    path('get_gifts/', views.api_load_response_data),
    path('gift_consumption/', views.api_create_checkout_session),
    path('webhooks/stripe/', views.stripe_webhook_view, name='stripe-webhook'),
    path("selected_gifts/", views.selected_gifts_list, name="selected_gifts"),
    path('create_user/', views.api_create_user),
    re_path('login/', views.api_login),
    re_path('check_authentication/', views.api_check_authentication),
    path('confirm-email/', views.confirm_email_view),
]
