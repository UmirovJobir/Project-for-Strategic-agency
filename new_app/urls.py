from django.urls import path
from .views import Detail, Country_view, Product_view, Data_1_modul


urlpatterns = [
    path('detail/', Detail.as_view()),
    path('products/', Product_view.as_view()),
    path('countries/', Country_view.as_view()),
    path('data/', Data_1_modul.as_view()),
]