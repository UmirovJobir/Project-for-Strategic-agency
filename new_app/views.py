from .models import (
    Product, Detail, Country, 
    Gdp, Year, Import_export_for_db)
from .serializers import (
    Detail_serializer, Product_serializer, 
    Country_serializer, Product_serializer_details,
    DetailForSumSerializer,UserSerializer,RegisterSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.core.exceptions import SuspiciousOperation
from new_app.libs.psql import db_clint
import pandas as pd
from logic import first_modul_main, second_modul_main
from get_data import (
    get_data__product_data_for_db,
    get_data__import_export_for_db,
    get_data__gdp_for_db,
    get_data__X_and_C_for_db,
    get_data__matrix_db
)
import math
import warnings
warnings.filterwarnings('ignore')


#API to register user
class RegisterUserView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

#API to Get User Details using Token Authentication
class UserDetailView(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  def get(self,request,*args,**kwargs):
    print(request.user.id)
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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        city = request.GET.get('country_id')
        city = city.split(",")
        countries = Country.objects.filter(pk__in=city)
        products = Product.objects.filter(details__country__in=countries).distinct()
        serializer = Product_serializer(products, many=True)        
        return Response(serializer.data)


# Data of products with user choosed by counties which he/she wants to see
class DetailView(APIView):
    permission_classes = (IsAuthenticated,)

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
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        country_id = request.data['country_id']
        product_id = request.data['product_id']
        duties = request.data['duty']
        year = request.data['year']
        export_percentage = request.data['export_percentage']
        import_percentage = request.data['import_percentage']

        url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
        response = requests.get(url)
        res = response.json()
        USD = float(res[0]['Rate'])

        exchange_rate = USD 
        
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

        skp_values = {'A01': 'Продукция сельского хозяйства, охоты и услуги в этих областях', 
        'A02': 'Продукция лесного хозяйства, лесозаготовок и услуги в этих областях', 
        'A03': 'Рыба и прочая продукция рыболовства; продукция рыбоводства; услуги связанные с рыболовством и рыбоводством', 
        'B05': 'Уголь каменный и уголь бурый (лигнит)', 'B06': 'Нефть сырая и газ природный', 
        'B07': 'Руды металлические', 'B08': 'Продукция добычи прочих полезных ископаемых ', 
        'B09': 'Услуги в области добычи полезных ископаемых', 'C10': 'Продукты пищевые', 
        'C11': 'Напитки ', 'C12': 'Изделия табачные', 'C13': 'Текстиль и текстильные изделия', 
        'C14': 'Одежда', 'C15': 'Кожа и  изделия из кожи', 
        'C16': 'Древесина и изделия из древесины и пробки (кроме мебели); изделия из соломки и материалов для плетения ', 
        'C17': 'Бумага и изделия из бумаги', 'C18': 'Услуги печатные и услуги по воспроизведению записанных материалов', 
        'C19': 'Кокс и продукты переработки нефти ', 'C20': 'Продукция химическая ', 'C21': 'Продукты фармацевтические основные и препараты фармацевтические', 
        'C22': 'Изделия резиновые и пластмассовые ', 'C23': 'Изделия минеральные неметаллические прочие', 'C24': 'Металлы основные', 
        'C25': 'Изделия металлические готовые, кроме машин и оборудования', 'C26': 'Компьютеры, электронное и оптическое оборудование', 
        'C27': 'Оборудование электрическое ', 'C28': 'Машины и оборудование, не включенные в другие группировки', 'C29': 'Автотранспортные средства, прицепы и полуприцепы', 
        'C30': 'Прочие транспортные средства и оборудование', 'C31': 'Мебель', 'C32': 'Продукция прочая', 'C33': 'Услуги по ремонту и установке  машин и оборудования', 
        'D35': 'Электроэнергия, газ, пар и кондиционированный воздух', 'E36': 'Вода природная; услуги по обработке воды и водоснабжению ', 
        'E37': 'Услуги канализационных систем; шлам сточных вод', 'E38': 'Услуги по сбору, обработке и удалению отходов; услуги по утилизации отходов', 
        'E39': 'Услуги по рекультивации и прочие услуги в области удаления отходов', 'F': 'Сооружения и работы строительные', 
        'G': 'Услуги оптовой и розничной торговли, ремонт транспортных средств и мотоциклов', 'H49-51': 'Услуги по перевозкам', 
        'H52': 'Услуги по складированию и вспомогательные транспортные услуги ', 'H53': 'Услуги почтовые и курьерские ', 'I55': 'Услуги проживания', 
        'I56': 'Услуги по предоставлению продуктов питания и напитков', 'J58': 'Услуги издательские', 
        'J59': 'Услуги по производству кино-, видеофильмов и телевизионных программ, услуги по звукозаписи и изданию музыкальных произведений', 
        'J60': 'Услуги по составлению программ и телерадиовещанию', 'J61': 'Услуги телекоммуникационные ', 
        'J62': 'Услуги по компьютерному программированию, консультационные и другие сопутствующие услуги', 'J63': 'Услуги в области информации ', 
        'K64': 'Услуги финансовые, кроме услуг по страхованию и пенсионному обеспечению', 
        'K65': 'Услуги по страхованию, перестрахованию и пенсионному обеспечению, кроме услуг по обязательному социальному страхованию', 
        'K66': 'Услуги, вспомогательные по отношению к финансовым и страховым услугам', 'L68': 'Услуги, связанные с недвижимым имуществом  ', 
        'M69': 'Услуги в области права и бухгалтерского учета', 'M70': 'Услуги головных компаний; услуги консультационные по вопросам управления ', 
        'M71': 'Услуги в области архитектуры, инженерных изысканий, технических испытаний и анализа  ', 'M72': 'Услуги по научным исследованиям и разработкам', 
        'M73': 'Услуги в области рекламы и изучения конъюнктуры рынка', 'M74': 'Услуги профессиональные, научные и технические прочие', 'M75': 'Услуги ветеринарные ', 
        'N77': 'Услуги по аренде и лизингу', 'N78': 'Услуги по трудоустройству  ', 
        'N79': 'Услуги туристических агентств, туроператоров и прочие услуги по бронированию и связанные с ними услуги  ', 
        'N80': 'Услуги по обеспечению безопасности и проведению расследований  ', 'N81': 'Услуги по обслуживанию зданий и благоустройству ландшафта', 
        'N82': 'Услуги в области административно-управленческого, хозяйственного и прочего вспомогательного обслуживания', 
        'O84': 'Услуги в области государственного управления и обороны; услуги по обязательному социальному обеспечению', 'P85': 'Услуги в области образования', 
        'Q86': 'Услуги в области здравоохранения ', 'Q87': 'Услуги по предоставлению ухода с обеспечением проживания', 'Q88': 'Услуги социальные без обеспечения проживания', 
        'R90': 'Услуги в области творчества, искусства и развлечений', 'R91': 'Услуги библиотек, архивов, музеев и прочие услуги в области культуры', 
        'R93': 'Услуги в области спорта и организации развлечений и отдыха  ', 'S94': 'Услуги, предоставляемые членскими организациями', 
        'S95': 'Услуги по ремонту компьютеров, предметов личного пользования и бытовых товаров', 'S96': 'Услуги индивидуальные почие'}


        elasticity_dict = {}
        for i, j in zip(skp, first_modul['elasticity']):
            for a,b in skp_values.items():
                if a==i:
                    elasticity_dict[b] = j

        return Response(data={"first_modul":{"imp":first_modul['imp'], "elasticity":elasticity_dict},"second_modul":second_modul})


#API for show sum of all products prices by country id wich user gives 
class ProductPricesSumView(APIView):   
    permission_classes = (IsAuthenticated,)
        
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

import requests
from pprint import pprint

class Money(APIView):
    def get(self, request):
        url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'
        response = requests.get(url)
        pprint(response.status_code)
        res = response.json() #['conversion_rate']
        a = res[0]['Rate']
        a = float(a)
        return Response(data={"USD":a})
