# from django.shortcuts import render
# from rest_framework.views import APIView
# from serializers import VendorsSerializer
# from store.models import Product
# from rest_framework.response import Response
# import json

# # Create your views here.

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

# class RestaurantLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         if not user.is_active:
#             return Response({'error': 'Your account is not active.'}, status=400)
#         return Response({'token': token.key})

# from rest_framework import generics, permissions
# from .models import DailyMenu
# from .serializers import DailyMenuSerializer
# # from .tasks import process_daily_menu
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# class DailyMenuView(generics.CreateAPIView):
#     queryset = DailyMenu.objects.all()
#     serializer_class = DailyMenuSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         daily_menu = serializer.save(restaurant=self.request.user)

#         # Use Celery to process the daily menu asynchronously
#         process_daily_menu.delay(daily_menu.id)

#         # Use Django Channels to fetch related data asynchronously
#         channel_layer = get_channel_layer()
#         for item in daily_menu.items.all():
#             async_to_sync(channel_layer.send)(
#                 "fetch-related-data",
#                 {
#                     "type": "fetch_related_data",
#                     "item_id": item.id
#                 }
#             )


# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import MenuItem
# from asgiref.sync import async_to_sync, database_sync_to_async

# class FetchRelatedDataConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add(
#             "fetch-related-data-group",
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             "fetch-related-data-group",
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         item_id = text_data_json["item_id"]
#         item = await database_sync_to_async(MenuItem.objects.get)(id=item_id)
#         await database_sync_to_async(item.fetch_related_data)()

# # daphne myproject.asgi:application -b 0.0.0.0 -p 8001


# from rest_framework import generics, permissions
# from .models import Order
# from .serializers import OrderSerializer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# class CheckOrdersView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         # Use Django Channels to fetch orders asynchronously
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.send)(
#             "fetch-orders",
#             {
#                 "type": "fetch_orders",
#                 "restaurant_id": self.request.user.id
#             }
#         )
#         return Order.objects.filter(restaurant=self.request.user)
 

# from channels.generic.websocket import AsyncWebsocketConsumer
# # from .models import Order

# # class FetchOrdersConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         await self.channel_layer.group_add(
# #             "fetch-orders-group",
# #             self.channel_name
# #         )
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         await self.channel_layer.group_discard(
# #             "fetch-orders-group",
# #             self.channel_name
# #         )

# #     async def receive(self, text_data):
# #         text_data_json = json.loads(text_data)
# #         restaurant_id = text_data_json["restaurant_id"]
# #         orders = await database_sync_to_async(Order.objects.filter)(restaurant_id=restaurant_id)
# #         serializer = OrderSerializer(orders, many=True)
# #         await self.send(text_data=json.dumps(serializer.data))


# # daphne myproject.asgi:application -b 0.0.0.0 -p 8002



# # class VendorsView(APIView):
# #     def get(self, request, format=None):
# #         ven_id = request.get('restaurant_id', None)
# #         restro = Product.objects.filter(vendor_id = ven_id)
# #         serializer = VendorsSerializer(restro, many =True)
# #         return Response(serializer.data)
