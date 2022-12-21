from django.urls import path
from .views import DetailView, CountryView, ProductView, DataView, SaveDataView, ProductPricesSumView


urlpatterns = [
    path('detail/', DetailView.as_view()),
    path('products/', ProductView.as_view()),
    path('countries/', CountryView.as_view()),
    path('data/', DataView.as_view()),
    path('save/', SaveDataView.as_view()),
    path('price_sum/', ProductPricesSumView.as_view())
]