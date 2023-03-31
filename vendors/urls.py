# urls.py

from django.urls import path
from .celery_view import login, upload_menu, restaurant_onboarding, IncomingOrderView

urlpatterns = [
    path('login/', login, name='login'),
    # path('restaurants/<int:restaurant_id>/orders/', get_orders, name='get_orders'),
    path('restaurants/<int:restaurant_id>/menu/', upload_menu, name='upload_menu'),
    path('restaurants/register/', restaurant_onboarding, name='restaurant_onboarding'),
    path('restaurants/incoming_orders/', IncomingOrderView.as_view(), name='incoming-orders'),

]
