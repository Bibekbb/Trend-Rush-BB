from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Brand(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.name
    

def Price_Positive(value):
    if value < 0:
        raise ValidationError("Price Can Not Be Negative.")

class Product(models.Model):
    Avaliability = (
        ('In Stock','In Stock'),
    ('Out of Stock','Out of Stock'),
    )


    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,default=None)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True, default=None)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ecommerce/prodimg')
    descriptions = models.TextField(default='')
    name = models.CharField(max_length=100)
    price = models.FloatField(validators=[Price_Positive])
    Avaliability = models.CharField(choices=Avaliability,max_length=100, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name




class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject= models.CharField(max_length=100)
    message = models.TextField()


    def __str__(self) -> str:
        return self.name
    



class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=100,default="none")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default="none")
    quantity = models.CharField(max_length=10)
    total = models.FloatField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)


    def __str__(self) -> str:
        return self.product



class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10)  # E.g., 'cart', 'purchase', 'view', etc.

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.interaction_type}"




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
