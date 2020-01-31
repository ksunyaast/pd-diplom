from django.contrib import admin
from django.urls import path, include

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, ShopView, CategoryView

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('shops', ShopView.as_view(), name='shop-view'),
    path('category', CategoryView.as_view(), name='category-view'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
]
