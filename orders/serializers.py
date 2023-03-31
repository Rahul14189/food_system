from rest_framework import serializers
from .models import Order
from store.models import Product
# from django.contrib.auth.models import User


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'