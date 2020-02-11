import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from requests import get
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader

# Create your views here.
from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, ConfirmEmailToken

from backend.serializers import ShopSerializer, CategorySerializer, UserSerializer, ProductSerializer,\
    ProductInfoSerializer


# Регистрация
class RegisterAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.data._mutable = True
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """
    # Регистрация методом POST
    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


#Авторизация
class LoginAccount(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(username=request.data['email'], password=request.data['password'])
            print(user)
            if user is not None:
                token_query = Token.objects.filter(user=user.pk)
                if token_query.exists():
                    key = token_query.values_list('key', flat=True).get()
                else:
                    key = Token.objects.create(user=user).key
                return JsonResponse({'Status': True, 'Token': key})
        return JsonResponse({'Status': False, 'Login': 'Failed'}, status=400)



# Обновление прайса
class PartnerUpdate(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Необходимо авторизоваться'}, status=403)
        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
        file = request.data['file']
        if file:
            validate_url = URLValidator()
            try:
                validate_url(file)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(file).content
                data = load_yaml(stream, Loader=Loader)
                filename = file.split('/')[-1]
                shop, _ = Shop.objects.get_or_create(name=data['shop'], url=file, filename=filename)
                for category in data['categories']:
                    category_item, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_item.shops.add(shop)
                    category_item.save()
                ProductInfo.objects.filter(shop=shop).delete()
                for product in data['goods']:
                    product_category = Category.objects.get(id=product['category'])
                    product_item, _ = Product.objects.get_or_create(name=product['name'],
                                                                    category=product_category)
                    product_item.save()
                    product_info = ProductInfo.objects.create(external_id=product['id'],
                                                              name=product['name'],
                                                              product=product_item,
                                                              shop=shop,
                                                              quantity=int(product['quantity']),
                                                              price=int(product['price']),
                                                              price_rrc=int(product['price_rrc']))
                    for name, value in product['parameters'].items():
                        parameter_item, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info=product_info,
                                                        parameter=parameter_item,
                                                        value=value)
                return JsonResponse({'Status': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


# Просмотр магазинов
class ShopView(ListAPIView):
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


# Просмотр категорий
class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Список товаров
class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Просмотр карточки товара
class ProductInfoView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = ProductInfo.objects.get(external_id=int(request.data['id']))
        serializer = ProductInfoSerializer(queryset)
        return Response(serializer.data)



class PartnerState(APIView):
    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Необходимо авторизоваться'}, status=403)
        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data)
