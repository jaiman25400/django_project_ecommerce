# Superuser jaiman17,1234

from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from django.db.models import Q
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class ProductQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = Q(name__icontains=query) | Q(category__name__icontains=query)

        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    description = models.TextField("Description", max_length=600)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, default=1)
    num_stock = models.IntegerField(default=0)

    objects = ProductManager()

    @staticmethod
    def get_product_by_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })


class ShippingAddress(models.Model):
    addressLine1 = models.CharField(max_length=200, null=False)
    addressLine2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    #order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.addressLine1)


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=10)
    alter_mobile_no = models.CharField(max_length=10)
    address = ManyToManyField(ShippingAddress)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    price = models.FloatField(default=False)

    #status = models.BooleanField(default=False,null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_order_by_customer(customer_id):
        return Order\
            .objects\
            .filter(profile=customer_id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_final_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        total += total * (18/100)
        return total

    @property
    def get_tax(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        tax = total * (18/100)
        return tax


class OrderItem(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    #category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,default=1)

    def __str__(self):
        return str(self.order_id)

    @property
    def get_total(self):
        total = float(self.product.price) * float(self.quantity)
        return total

    @staticmethod
    def get_orderitem_by_customer(customer_id):
        return OrderItem\
            .objects\
            .filter(profile=customer_id)
