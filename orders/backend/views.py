import json

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from requests import get
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as load_yaml, Loader

# Create your views here.
from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class RegisterAccount(APIView):
    pass


class LoginAccount(APIView):
   pass


class PartnerUpdate(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
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
                    product_info = ProductInfo.objects.create(name=product['name'],
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
