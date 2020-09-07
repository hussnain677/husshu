from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):

    CONDITION_TYPE = {
        ("New" , "New") ,
        ("used" , "Used")
    }


    # contain all the products information
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length = 100)
    description = models.TextField(max_length = 500)
    category = models.ForeignKey("Category" , on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length = 100)
    condition = models.CharField(max_length = 100, choices= CONDITION_TYPE)
    price = models.CharField(max_length = 12)
    image = models.FileField(upload_to='main_product/', blank=True, null=True)
    created = models.DateTimeField(default = timezone.now)
    number = models.CharField(max_length = 12)
    city = models.CharField(max_length = 20)
    country = models.CharField(max_length = 20)
    slug = models.SlugField(blank=True, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug and self.product_name :
            self.slug = slugify(self.product_name)
        super(Product , self).save(*args, **kwargs)


# for see name of model
    
    def __str__(self):
        return self.product_name + " | " + str(self.user.username)




class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='product/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'product Image'
        verbose_name_plural = 'Product Images'


# for see name of model
    def __str__(self):
        return self.product.product_name  




class Category(models.Model):
    # for product category main screen show
    category_name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='category/', blank=True, null=True)


    slug = models.SlugField(blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name :
            self.slug = slugify(self.category_name)
        super(Category , self).save(*args, **kwargs)


# change category name into plural
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'



# for see name of model
    
    def __str__(self):
        return self.category_name
        
class Viewer(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ip = models.TextField(default=None)
    def __str__(self):
        return self.product.product_name