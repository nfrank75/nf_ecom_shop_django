from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'


class PaymentStatus(models.TextChoices):
    PAID = 'PAID'
    UNPAID = 'UNPAID'
    
class PaymentMode(models.TextChoices):
    COD = 'COD'
    CARD = 'CARD'

class Order(models.Model):
    street = models.CharField(max_length=100, default="", blank=False)
    city = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.IntegerField(default=0)

    payment_status = models.CharField(max_length=50, 
                                      choices=PaymentStatus.choices,
                                      default=PaymentStatus.UNPAID,
                                      )
    
    status = models.CharField(max_length=50, 
                                      choices=OrderStatus.choices,
                                      default=OrderStatus.PROCESSING,
                                      )
    
    payment_mode = models.CharField(max_length=50, 
                                      choices=PaymentMode.choices,
                                      default=PaymentMode.COD,
                                      )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    createdAt = models.DateTimeField(auto_now_add = True)

    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-createdAt',)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return 'Order ID : ' + str(self.id) + self.user.username


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='orderitems')
    name = models.CharField(max_length=50, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    createdAt = models.DateTimeField(auto_now_add = True)
    is_active = models.BooleanField(default=True)

    
    class Meta:
        ordering = ('-createdAt',)
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return self.name
    