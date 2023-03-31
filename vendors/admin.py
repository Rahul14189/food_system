from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Restaurant, RestaurantModel

# Register your models here.
class RestaurantManager(UserAdmin):
    # list_display = ['name','last_name','username','email','last_login']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Restaurant)
