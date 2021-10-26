from django.urls import path

from base.views import profile_views as views

'''
CLIENT
Base ENDPOINT /api/profiles/
'''
urlpatterns = [
    path('<str:username>/', views.profile_detail_api_view),
    path('<str:username>/connect/', views.profile_detail_api_view),
]