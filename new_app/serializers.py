
from pyexpat import model
from requests import request
from rest_framework import serializers
from .models import Product, Detail, Country, Year
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name"]

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  confirm_password = serializers.CharField(write_only=True, required=True)

  class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {'first_name': {'required': True},'last_name': {'required': True}}

  def validate(self, attrs):
    if attrs['password'] != attrs['confirm_password']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
        username=validated_data['first_name'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user



class Year_serializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('year',)


class Country_serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'country_name',)


class Product_serializer(serializers.ModelSerializer):
    countries = Country_serializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'countries')
 

class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(country__in=self.context['request'].data['country_id'])
        print(data)
        return super(FilteredListSerializer, self).to_representation(data)

class Detail_serializer(serializers.ModelSerializer):
    # year = Year_serializer(read_only=True)
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Detail
        fields = ('price', 'duty', 'year', 'country')

class Product_serializer_details(serializers.ModelSerializer):
    details = Detail_serializer(many=True, read_only=True) # source="current_epg")
    countries = Country_serializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('product_name', 'details', 'countries')
    
    # def create(self, validated_data):
    #     details_data = validated_data.pop('details')
    #     detail = Detail.objects.create(**validated_data)
    #     for detail_data in details_data:
    #         Detail.objects.create(details=detail, **detail_data)
    #     return detail


class DetailForSumSerializer(serializers.ModelSerializer):
    year = Year_serializer(read_only=True) 
    class Meta:
        model = Detail
        fields = ('price', 'duty','year','product','country')