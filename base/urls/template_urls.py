from django.urls import path
from base.views import template_views as views


urlpatterns = [
    path('', views.getTemplates, name="templates"),
    path('<str:pk>/', views.getTemplate, name="template"),  
]