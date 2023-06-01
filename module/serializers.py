
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
    fields = ["id", "username", "first_name", "last_name", "email"]

class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField()
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  confirm_password = serializers.CharField(write_only=True, required=True)

  class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {'first_name': {'required': True},'last_name': {'required': True}}

  def validate(self, attrs):
    if attrs['password'] != attrs['confirm_password']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
        username=validated_data['username'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        email=validated_data['email']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user



class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('year',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'country_name',)


class ProductSerializer(serializers.ModelSerializer):
    countries = CountrySerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'product_name', 'countries')
 

class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(country__in=self.context['request'].data['country_id'])
        return super(FilteredListSerializer, self).to_representation(data)

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Detail
        fields = ('price', 'duty', 'year', 'country')

class ProductDetailSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('product_name', 'details', 'countries')


class DetailForSumSerializer(serializers.ModelSerializer):
    year = YearSerializer(read_only=True) 
    class Meta:
        model = Detail
        fields = ('price', 'duty','year','product','country')