from django.db import models
import uuid


# Create your models here.
class Register(models.Model):
    uname=models.CharField(max_length=50)
    email=models.EmailField()
    mobno=models.IntegerField()
    passw=models.CharField(max_length=50)

    def __str__(self):
        return self.email

class Category(models.Model):
    category=models.CharField(max_length=50)
    category_image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.category

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    product_image=models.ImageField(upload_to='images/')
    product_description=models.TextField()



    def __str__(self):
        return self.product_name




class Carts(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    products=models.ForeignKey(Product, on_delete=models.CASCADE)
    orderid=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    quantity=models.PositiveIntegerField(default=0)
    total_price=models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.orderid

class Order(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    orderid=models.CharField(max_length=500)
    prod=models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='images/')
    quantity=models.IntegerField()
    country=models.CharField(max_length=50)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zipcode=models.CharField(max_length=50)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=50)
    total_price=models.IntegerField(default=0)
    deliverytype=models.CharField(max_length=50)


class Card(models.Model):
    user=models.ForeignKey(Register, on_delete=models.CASCADE)
    cardnumber = models.IntegerField(default=0, null=True, blank=True)
    cardholder = models.CharField(max_length=50, null=True, blank=True)
    expirationdate = models.DateField(null=True, blank=True)
    ccv = models.IntegerField(default=0, null=True, blank=True)

class Contact(models.Model):
    fname=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.TextField(max_length=600)