
from requests import request
from rest_framework import serializers
from .models import Product, Detail, Country

class Country_serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country_name',)

class Product_serializer(serializers.ModelSerializer):
    countries = Country_serializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'countries')
 
class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(country__in=self.context['request'].data['country_id'])
        return super(FilteredListSerializer, self).to_representation(data)

class Detail_serializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Detail
        fields = ('price', 'duty', 'year', 'country')

class Product_serializer_details(serializers.ModelSerializer):
    details = Detail_serializer(many=True, read_only=True) # source="current_epg")
    countries = Country_serializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('code_product', 'product_name', 'skp', 'details', 'countries')
    
    # def create(self, validated_data):
    #     details_data = validated_data.pop('details')
    #     detail = Detail.objects.create(**validated_data)
    #     for detail_data in details_data:
    #         Detail.objects.create(details=detail, **detail_data)
    #     return detail
    


