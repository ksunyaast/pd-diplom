from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from backend.views import PartnerUpdate, RegisterAccount, ConfirmAccount, LoginAccount, ShopView, CategoryView,\
     BasketView, OrderView, ContactView, ProductViewSet
    # ProductView, ProductInfoView

router = DefaultRouter()


urlpatterns = [
    path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    path('shops', ShopView.as_view(), name='shop-view'),
    path('category', CategoryView.as_view(), name='category-view'),
    # path('products', ProductView.as_view(), name='product-view'),
    # path('product-info', ProductInfoView.as_view(), name='product_info-view'),
    path('products-viewset/', ProductViewSet.as_view({'get': 'list'})),
    path('products-viewset/<int:pk>', ProductViewSet.as_view({'get': 'retrieve'})),
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/login', LoginAccount.as_view(), name='user-login'),
    path('user/contact', ContactView.as_view(), name='user-contact'),
    path('basket', BasketView.as_view(), name='basket'),
    path('order', OrderView.as_view(), name='order'),
]
