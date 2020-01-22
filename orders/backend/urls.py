from django.contrib import admin
from django.urls import path, include

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
]
