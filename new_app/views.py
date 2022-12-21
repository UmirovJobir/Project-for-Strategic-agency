from wsgiref.util import request_uri
from rest_framework import permissions
from .models import Product, Detail, Country, Gdp, Year, Import_export_for_db
from .serializers import Detail_serializer, Product_serializer, Country_serializer, Product_serializer_details, DetailForSumSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import SuspiciousOperation
from new_app.libs.psql import db_clint
import pandas as pd
from logic import first_modul_main, second_modul_main
from get_data import (
    get_data__countries_data_for_db,
    get_data__import_export_for_db,
    get_data__gdp_for_db,
    get_data__X_and_C_for_db,
    get_data__matrix_db
)
import math
import warnings
warnings.filterwarnings('ignore')


# All countries
class CountryView(APIView): 
    def get(self, request):
        countries = Country.objects.all()
        serializer = Country_serializer(countries, many=True)
        return Response(serializer.data)

# Filtered products by countries with user choosed
class ProductView(APIView):
    def get(self, request):
        city = request.GET.get('country_id')
        city = city.split(",")
        countries = Country.objects.filter(pk__in=city)
        products = Product.objects.filter(details__country__in=countries).distinct()
        serializer = Product_serializer(products, many=True)        
        return Response(serializer.data)


# Data of products with user choosed by counties which he/she wants to see
class DetailView(APIView):
    def get(self, request):  
        try:
            countries = request.data['country_id']
            products = Product.objects.filter(pk__in=request.data.get('product_id'))
            serializer = Product_serializer_details(products, many=True, context={'request': request, "country_id": countries})
            return Response(serializer.data)
        except (TypeError, KeyError):
            raise SuspiciousOperation('Invalid JSON')


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
        exchange_rate = request.data['exchange_rate']

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
            elasticity_dict[i] = j

        return Response(data={"first_modul":{"imp":first_modul['imp'], "elasticity":elasticity_dict},"second_modul":second_modul})


# API to save excel files (requires login password of admin)
class SaveDataView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        file_name = request.data['file_name']
        file = request.data['file']   
                
        if file_name=='products details file':
            count = get_data__countries_data_for_db(file)

        elif file_name=='gdp file':
            count = get_data__gdp_for_db(file)
        
        elif file_name=='import export file':
            count = get_data__import_export_for_db(file)
        
        elif file_name=='x c file':
            count = get_data__X_and_C_for_db(file)
        
        elif file_name=='matrix file':
            count = get_data__matrix_db(file)
        
        else:
            content = {'ERROR': 'Name of the file unknown.' 
            'You can send excel file named '
                'products details file, '
                'gdp file, '
                'import export file, '
                'x c file, '
                'matrix file'}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        
        if type(count) == str:
            if count == "0, all data is exist":
                return Response(data={"created data": f"{count}"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data={"created data": f"{count}"})
        elif type(count) == int:
            if count == 0:
                return Response(data={"created data": f"{count}, all data is exist"}, status=status.HTTP_404_NOT_FOUND)
            elif count > 0:
                return Response(data={"created data": f"{count}"})


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
