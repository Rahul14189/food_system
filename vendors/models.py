from django.db import models
from app.models import Account
# Create your models here.

class RestaurantModel(models.Model):
    ActiveOrNot = {
        ('Yes', 'Yes'),
        ('No', 'No'),
    }
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    area_pincode = models.IntegerField()
    email = models.EmailField(max_length=20)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    is_active = models.CharField(max_length=10, choices=ActiveOrNot, default="Yes")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    def area_pin(self):
        return f'{self.area_pincode}'

    def __str__(self):
        return self.name


from django.db import models
# from django.contrib.auth.models import User
from app.models import Account
class Restaurant(models.Model):
    # user = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.IntegerField(blank=True)
    location = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, unique=True, null=True, default=1, blank=True)
    onboarding_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name




from django.contrib.auth.models import User


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('PENDING', 'Pending'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('COMPLETED', 'Completed'),
#         ('CANCELLED', 'Cancelled'),
#     )

#     restaurant = models.ForeignKey(Account, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Account, on_delete=models.CASCADE)
#     delivery_boy = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
#     table_id = models.CharField(max_length=50, null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     address = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     special_request = models.TextField(null=True, blank=True)
#     delivery_time = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
