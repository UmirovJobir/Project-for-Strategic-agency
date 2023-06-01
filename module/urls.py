from django.urls import path
from .views import (
    DetailView, CountryView, 
    ProductView, DataView, 
    ProductPriceSumView,
    UserDetailView,RegisterUserView)

urlpatterns = [
    path('details/', DetailView.as_view()),
    path('products/', ProductView.as_view()),
    path('countries/', CountryView.as_view()),
    path('data/', DataView.as_view()),
    path('price_sum/', ProductPriceSumView.as_view()),
    path('user_details/',UserDetailView.as_view()),
    path('register/',RegisterUserView.as_view()),
]

