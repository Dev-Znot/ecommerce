from django.db import models
from django.utils.html import mark_safe

from shortuuid.django_fields import ShortUUIDField
from userauths.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

import random


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)
STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in review", "In Review"),
    ("published", "Published"),
)
RATING = (
    (1 , "★☆☆☆☆"),
    (2 , "★★☆☆☆"),
    (3 , "★★★☆☆"),
    (4 , "★★★★☆"),
    (5 , "★★★★★"),
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefghi1234")
    title = models.CharField(max_length=100, default="Jewelery")
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefghi1234")

    title = models.CharField(max_length=100, default="Nest")
    image = models.ImageField(upload_to=user_directory_path, default="Vendor.jpg")
    description = models.TextField(null=True, blank=True, default="Amazing vendor")

    address = models.CharField(max_length=50, default="123 Main Street")
    contact = models.CharField(max_length=50, default="+123 (456) 789")
    chat_resp_time = models.CharField(max_length=50, default="100")
    shipping_on_time = models.CharField(max_length=50, default="100")
    authentic_rating = models.CharField(max_length=50, default="100")
    day_return = models.CharField(max_length=50, default="100")
    warranty_period = models.CharField(max_length=50, default="100")

    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True )


    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefghi1234")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100, default="Fresh Pear")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="this is the product")

    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default="2.99", null=True, blank=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    specifications = models.TextField(null=True, blank=True)
 #   tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(max_length=10, choices=STATUS, default="in review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="abcdefghi1234")

    date = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

    def get_porcentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price



class Productimages(models.Model):
    images = models.ImageField(upload_to="products-images", default="products.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product images"


######################################### Order, Cart ###########################################


class Coupons(models.Model):
    series = models.IntegerField(default=0)
    tag = models.CharField( max_length=50)

    def save(self, *args, **kwargs):
        if not self.series:
            self.series = random.randint(1000, 9999)
        super().save(*args, **kwargs)


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="processing")

    class Meta:
        verbose_name_plural = "Cart order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    invoice_no = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=5, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart order items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    


############################## Products review, whishlist, Address ##############################


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Reviews"
    
    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"
    
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=50, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


#################################### Blog #######################################################

class Blog(models.Model):
    image = models.ImageField(upload_to="blog/", null=False)
    title = models.CharField(max_length=50)
    summary = RichTextField()
    date = models.CharField(max_length=5, null=False)

    content = RichTextUploadingField()
   

##################################### Contact ###################################################

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    assunto = models.CharField(max_length=50)
    texto = models.TextField()

    def __str__(self):
        return self.name
    












