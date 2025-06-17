from django.urls import path

from .views import *


urlpatterns = [
    path('login/',login,name='login'),
    path('logout/',logout,name='login'),
    path('password-reset/',password_reset,name='password-reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/',password_reset_confirm,name='password-reset-confirm'),
]
