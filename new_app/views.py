from .models import (
    Product, Detail, Country, SkpValues
    )
from .serializers import (
    Detail_serializer, Product_serializer, 
    Country_serializer, Product_serializer_details,
    UserSerializer,RegisterSerializer
    )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.models import User
from logic import first_modul_main, second_modul_main
from new_app.libs.API import get_exchange_rate
import math
import warnings
warnings.filterwarnings('ignore')


#API to register user
class RegisterUserView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

#API to Get User Details using Token Authentication
class UserDetailView(APIView):
  permission_classes = (IsAdminUser, IsOwnerOrReadOnly)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# All countries
class CountryView(APIView): 
    def get(self, request):
        countries = Country.objects.all()
        serializer = Country_serializer(countries, many=True)
        return Response(serializer.data)

# Filtered products by countries with user choosed
class ProductView(APIView):
    def get(self, request):
        try:
            countries = request.GET.get('country_id')
            countries = countries.split(",")
        except:
            return Response(data={"error": "country_id parametr is not given"}, status=status.HTTP_400_BAD_REQUEST)
        
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
        serializer = Product_serializer(products, many=True)        
        return Response(serializer.data)


# Data of products with user choosed by counties which he/she wants to see
class DetailView(APIView):
    def get(self, request):  
        try:
            countries_list = request.data['country_id']
            products_list = request.data['product_id']

            products = Product.objects.filter(pk__in=products_list)
            serializer = Product_serializer_details(products, many=True, context={'request': request, "country_id": countries_list})
            return Response(serializer.data)
        except (TypeError, KeyError):
            return Response(data={"error":f"countries_lis or products_list is not given!"},
                            status=status.HTTP_400_BAD_REQUEST)


#API for show sum of all products prices by country id wich user gives 
class ProductPricesSumView(APIView):           
    def get(self, request):
        countries = request.data['country_id']
        last_year_in_details = Detail.objects.all().last().year
        price_sum = {}
        for country_id in countries:
            details = Detail.objects.filter(country=country_id,year=last_year_in_details)
            country = Country.objects.get(id=country_id).country_name
            price_list = []
            for detail in details:
                if detail.price is not None:
                    price_list.append(detail.price)
            price_sum[country]=math.fsum(price_list)
        return Response(price_sum) 
    

# Logical part of project.
# API gets request (country_id, product_id, duties, year, percent, exchange_rate, percent) and response a future data of skp
class DataView(APIView):   
    def post(self, request):
        country_id = request.data['country_id']
        product_id = request.data['product_id']
        duties = request.data['duty']
        year = request.data['year']
        export_percentage = request.data['export_percentage']
        import_percentage = request.data['import_percentage']
        
        last_detail_year = Detail.objects.last().year

        if year - int(f"{last_detail_year}") != len(duties):
            return Response(data={"error":f"duty length is not equal year from 2019 since {year}"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            #Get current dollar currency from The Central Bank's API
            exchange_rate = get_exchange_rate() 
            
            countries = []
            products = []
            skp = []

            export_percentage = export_percentage/100
            import_percentage = import_percentage/100

            for country in country_id:
                name = Country.objects.filter(id=country).values()
                for i in name:
                    countries.append(i.get('country_name'))
            for product in product_id:
                name = Product.objects.filter(id=product).values()
                for i in name:
                    if i.get('skp') in skp:
                        products.append(i.get('product_name'))
                    else:
                        skp.append(i.get('skp'))
                        products.append(i.get('product_name'))
            
            first_modul = first_modul_main(countries, skp, products, duties, year, import_percentage, exchange_rate)
            second_modul = second_modul_main(first_modul['imp'], year, skp, import_percentage, export_percentage)


            elasticity_dict = {}
            for i, j in zip(skp, first_modul['elasticity']):
                skp = SkpValues.objects.get(code=i)
                if i==skp.code:
                    elasticity_dict[skp.name] = j

            return Response(data={"first_modul":{"imp":first_modul['imp'], "elasticity":elasticity_dict},"second_modul":second_modul})


   



