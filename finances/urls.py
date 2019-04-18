from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list_transactions, name='list'),
    path('add_transaction/', views.add_transaction, name='addtr'),
    path('add_account/', views.add_account, name='addac'),
]