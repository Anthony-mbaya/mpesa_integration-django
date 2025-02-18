from django.urls import path
from mpesa_api_app import views #import views to access the def

app_name = "mpesa_api_app"

urlpatterns = [
    path('get_token/', views.get_token_view, name='get_token'),
    path('stk_push/', views.stk_push, name='stk_push'),
    path('mpesa_stk_push/', views.form, name='mpesa_stk_push'),
]