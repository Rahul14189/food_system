# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import RestaurantModel
from store.models import Product as Menu
from .serializers import MenuSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status



@shared_task
def upload_menu_task(restaurant_id, menu_data):
    try:
        restaurant = RestaurantModel.objects.get(id=restaurant_id)
        menu = Menu(restaurant=restaurant, items=menu_data)
        menu.save()
        
        # Send update to WebSocket clients
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"restaurant_{restaurant_id}",
            {
                "type": "menu_update",
                "menu": MenuSerializer(menu).data
            }
        )
        
        return True
    except ObjectDoesNotExist:
        return False

@csrf_exempt
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'User is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# @csrf_exempt
# @api_view(['GET'])
# def get_orders(request, restaurant_id):
#     try:
#         orders = Order.objects.filter(restaurant_id=restaurant_id)
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)
#     except ObjectDoesNotExist:
#         return Response({'success': False, 'message': 'Restaurant not found'})

@csrf_exempt
@api_view(['POST'])
def upload_menu(request, restaurant_id):
    menu_data = request.data.get('menu')
    if menu_data is None:
        return Response({'success': False, 'message': 'Menu data not provided'})
    
    # Process menu upload in background using Celery
    upload_menu_task.delay(restaurant_id, menu_data)
    
    return Response({'success': True, 'message': 'Menu uploaded successfully'})



from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .serializers import UserSerializer, RestaurantOnboardSerializer
from .models import Restaurant
from app.models import Account


@api_view(['POST'])
@permission_classes([AllowAny])
def restaurant_onboarding(request):
    """
    Register a new restaurant user and create a new restaurant record.
    """
    gst_number = request.data.get('gst_number')
    email = request.data.get('email')

    # Check if user with given GST number or email already exists
    if Account.objects.filter(username=gst_number).exists() or Account.objects.filter(email=email).exists():
        return Response({'error': 'User with given GST number or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        # Create a new user account
        user = user_serializer.save()
        # Create a new restaurant record with the user as the owner
        restaurant_serializer = RestaurantOnboardSerializer(data={
            'owner': user.id,
            'name': request.data.get('name'),
            'address': request.data.get('address'),
            'phone': request.data.get('phone'),
            'email': email,
            'location': request.data.get('location'),
            'gst_number': gst_number
        })
        if restaurant_serializer.is_valid():
            restaurant = restaurant_serializer.save()
            # Send login credentials to the restaurant owner's email
            subject = 'Your restaurant account has been created!'
            message = f'Your username is {user.username} and your password is {request.data.get("password")}.'
            from_email = 'shivamsuroc@gmail.com'  # Replace with your own email
            recipient_list = [user.email]
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Delete the user account if the restaurant record creation fails
            user.delete()
            return Response(restaurant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from orders.models import Order
from orders.serializers import OrderSerializer
# from .tasks import accept_order_task


from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from orders.models import Order
from rest_framework.views import APIView

@shared_task
def accept_order_task(order_id, message):
    order = Order.objects.get(id=order_id)
    order.status = 'accepted'
    order.save()
    
    # Send acceptance message to customer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'order_{order_id}',
        {
            'type': 'acceptance_message',
            'message': message
        }
    )


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IncomingOrderView(APIView):

    def get(self, request):
        orders = Order.objects.filter(restaurant=request.user.restaurant, status='pending')
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse({'orders': serializer.data})

    def post(self, request):
        order_id = request.POST.get('order_id')
        accept_order_task.delay(order_id, request.user.restaurant.id)
        return JsonResponse({'message': 'Order accepted successfully'})

    def put(self, request):
        order_id = request.POST.get('order_id')
        message = request.POST.get('message')
        location = request.POST.get('location')
        delivery_time = request.POST.get('delivery_time')
        order = Order.objects.get(id=order_id, restaurant=request.user.restaurant)
        order.status = 'accepted'
        order.message = message
        order.location = location
        order.delivery_time = delivery_time
        order.save()
        # Send real-time update to customers
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'order_{order.customer.id}',
            {
                'type': 'order.accepted',
                'message': message,
                'location': location,
                'delivery_time': delivery_time,
            }
        )
        return JsonResponse({'message': 'Order updated successfully'})
