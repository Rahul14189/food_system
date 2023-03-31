from rest_framework import serializers
from .models import RestaurantModel, Restaurant
from store.models import Product
# from django.contrib.auth.models import User
from app.models import Account


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantModel
        fields = '__all__'

class RestaurantOnboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


# class OrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Order
#         fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

