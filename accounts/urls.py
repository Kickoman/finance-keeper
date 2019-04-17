from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.sign_out, name='logout'),
]