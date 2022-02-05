from django.urls import path
from base.views import user_views as views



urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name='register'),
    path('profile/', views.getUserProfile, name="users-profile"),
    path('delete/', views.disableUser, name="user-disable"),
    path('reset_password', views.resetPasswordEmail, name='password-reset-email'),
    path('reset_password/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('reset_password_complete', views.SetNewPassword, name='password-reset-complete'),
    path('', views.getUsers, name="users"),  
]