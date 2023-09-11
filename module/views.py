import math
import warnings

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .libs import logic, API
from .models import Product, Detail, Country, SkpValues
from .serializers import (
    DetailSerializer, ProductSerializer, 
    CountrySerializer, ProductDetailSerializer,
    UserSerializer,RegisterSerializer
    )

warnings.filterwarnings('ignore')

class Logout(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


#API to register user
class RegisterUserView(CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


#API to Get User Details using Token Authentication
class UserDetailView(APIView):
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    print(user.auth_token)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# All countries
class CountryView(ListAPIView): 
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# Filtered products by countries with user choosed
class ProductView(APIView):
    def get(self, request):
        if "country_id" not in request.data:
            return Response(data={"error": "country ids is not given"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            countries = request.data['country_id']
            lst = []
            products = 0
            for i in countries:
                product = Product.objects.filter(details__country__id=i).distinct().order_by('id')
                lst.append(product)      
                if len(lst)==2:
                    query = lst[0].intersection(lst[1]).order_by('id')
                    if products == 0:
                        products = query
                    else:
                        products = products.intersection(query).order_by('id')
                    lst = []  
            if len(lst)!=0:
                    products = lst[0].intersection(products).order_by('id')
            # products = Product.objects.filter(details__country__in=countries).distinct().order_by('id')
            serializer = ProductSerializer(products, many=True)        
            return Response(serializer.data)


# Data of products with user choosed by counties which he/she wants to see
class DetailView(APIView):
    def get(self, request):  
        if ('country_id' not in request.data.keys()) or ('product_id' not in request.data.keys()):
            error = f"countries_list or products_list is not given!"
            return Response(data={"error":error}, status=status.HTTP_400_BAD_REQUEST)
        else:
            countries_list = request.data['country_id']
            products_list = request.data['product_id']
            
            products = Product.objects.filter(pk__in=products_list)
            serializer = ProductDetailSerializer(products, many=True, context={'request': request, "country_id": countries_list})
            return Response(serializer.data)



#API for show sum of all products prices by country id wich user gives 
class ProductPriceSumView(APIView):           
    def get(self, request):
        if "country_id" not in request.data.keys():
            return Response(data={"error": "country ids is not given"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            countries = request.data['country_id']
            last_year = Detail.objects.all().last().year
            price_sum = {}
            last_detail_year = Detail.objects.last().year
            for country_id in countries:
                details = Detail.objects.filter(country=country_id,year=last_year)
                country = Country.objects.get(id=country_id).country_name
                price_list = []
                for detail in details:
                    if detail.price is not None:
                        price_list.append(detail.price)
                price_sum[country]=math.fsum(price_list)
            return Response(data={"data":f"{price_sum,last_detail_year}"}) 
    

# Logical part of project.
# API gets request (country_id, product_id, duties, year, percent, exchange_rate, percent) and response a future data of skp
class DataView(APIView):   
    def post(self, request):
        try:
            country_id = request.data['country_id']
            product_id = request.data['product_id']
            year = request.data['year']
            duties = request.data['duty']
            export_percentage = request.data['export_percentage']
            import_percentage = request.data['import_percentage']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        last_detail_year = Detail.objects.last().year
        print(year-int(f"{last_detail_year}"))
        if year - int(f"{last_detail_year}") != len(duties):
            return Response(data={"error":f"duty length is not equal year from 2019 since {year}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #Get current dollar currency from The Central Bank's API
            exchange_rate = API.get_exchange_rate() 
            
            countries = []
            products = []
            skp = []

            export_percentage = export_percentage/100
            import_percentage = import_percentage/100

            for country in country_id:
                county_values = Country.objects.filter(id=country).values()
                for values in county_values:
                    countries.append(values.get('country_name'))

            for product in product_id:
                product_values = Product.objects.filter(id=product).values()
                for values in product_values:
                    if values.get('skp') in skp:
                        products.append(values.get('product_name'))
                    else:
                        skp.append(values.get('skp'))
                        products.append(values.get('product_name'))

            
            first_modul = logic.first_modul_main(countries, skp, products, duties, year, import_percentage, exchange_rate)
            second_modul = logic.second_modul_main(first_modul['imp'], year, skp, import_percentage, export_percentage)


            elasticity_dict = {}
            for i, j in zip(skp, first_modul['elasticity']):
                skp = SkpValues.objects.get(code=i)
                if i==skp.code:
                    elasticity_dict[skp.name] = j

            return Response(data={"first_modul":{"imp":first_modul['imp'], "elasticity":elasticity_dict},"second_modul":second_modul})


   



