from django.contrib import admin
from django.urls import path, include

from backend.views import PartnerUpdate, RegisterAccount, LoginAccount, ShopView, CategoryView, ProductView,\
    ProductInfoView

urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('shops', ShopView.as_view(), name='shop-view'),
    path('category', CategoryView.as_view(), name='category-view'),
    path('products', ProductView.as_view(), name='product-view'),
    path('product-info', ProductInfoView.as_view(), name='product_info-view'),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
]
