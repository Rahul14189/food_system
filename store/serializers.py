from rest_framework import serializers
from .models import Product


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'