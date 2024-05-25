from django.db import models
from django.contrib.auth.models import User
from django.db.models import  Sum,Avg,Count
from vendor.models import *
from vendor.utils import *
from PIL import Image,ImageOps
import os
from django.core.files.base import ContentFile
from io import BytesIO
import requests



class buyer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15,null=True)
    email = models.EmailField(max_length=200, null=True)
    email_verification_code = models.CharField(max_length=100, blank=True)
    email_isverified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    vendor_active_email = models.BooleanField(default=False)
    birthday = models.DateField(blank=True,null=True)
    code = models.CharField(max_length=12,blank=True)
    referred_by_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='buyer_referred_by')
    cusstomer_image = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    user_datecreated = models.DateTimeField(auto_now_add=True)
    user_dateupdated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def get_recoended_by(self, *args, **kwargs):
        pass
    
    def save(self, *args, **kwargs):
        if self.code == "" or self.email_verification_code == "":
            code = generate_ref_code()
            email_code = generate_email_verification_code()
            self.code = code
            self.email_verification_code = email_code
        super().save(*args,**kwargs)

    def total_order(self):
        total = 0
        for order in orders.objects.filter(cutomer_id = self.id):
            total += 1
        return total
    
    def get_cart_count(self):
        cart_ins = Cart.objects.get(user = self.user, is_paid=False)
        return cartItems.objects.filter(cart_ins=cart_ins).count()
    
    def get_wishlist(self):
        wishlist = favourite_items.objects.filter(favourite_ins = favourite.objects.get(user=self.user))
        pro_id = []
        for wishlist in wishlist:
            pro_id.append(wishlist.product.pk)
        return pro_id

class customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15,null=True)
    email = models.EmailField(max_length=200, null=True)
    email_verification_code = models.CharField(max_length=100, blank=True)
    email_isverified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    vendor_active_email = models.BooleanField(default=False)
    birthday = models.DateField(blank=True,null=True)
    code = models.CharField(max_length=12,blank=True)
    referred_by_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='customer_referred_by')
    cusstomer_image = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    user_datecreated = models.DateTimeField(auto_now_add=True)
    user_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_recoended_by(self, *args, **kwargs):
        pass
    
    def save(self, *args, **kwargs):
        if self.code == "" or self.email_verification_code == "":
            code = generate_ref_code()
            email_code = generate_email_verification_code()
            self.code = code
            self.email_verification_code = email_code
        super().save(*args,**kwargs)

    def total_order(self):
        total = 0
        for order in orders.objects.filter(cutomer_id = self.id):
            total += 1
        return total
    
    def total_product(self):
        total = 0
        for order in products.objects.filter(vendoraddedby = self.id):
            total += 1
        return total
    

class credit_cards(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False,null=False)
    card_no = models.IntegerField(blank=False,null=False)
    expiry = models.DateField()
    cvv = models.IntegerField(blank=False,null=False)
    date_created= models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return str(self.user)

class upi(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=50,blank=False,null=False)
    date_created= models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def  __str__(self):
        return str(self.user)
    
class bank_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=False,null=False)
    account_no = models.IntegerField(blank=False,null=False)
    ifsc_code = models.CharField(max_length=50,blank=False,null=False)
    
    def  __str__(self):
        return str(self.user)

class LastLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    browser_name = models.CharField(max_length=100,null=True, blank=True)
    device_name = models.CharField(max_length=100,null=True, blank=True)
    last_login_timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.user)

class address(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null =True)
    name = models.CharField(max_length=50, null= True)
    email = models.CharField(max_length=50, null = True)
    phone = models.IntegerField(null=True)
    abline1 = models.CharField(max_length=200, null=True)
    abline2 = models.CharField(max_length=200, null=True)
    abline3 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zip = models.IntegerField(null=False)
    isactive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class category(models.Model):
    itmclass = models.CharField(max_length=50,null=True)
    classname = models.CharField(max_length=50,null=True)
    category_image = models.ImageField(upload_to='images/categories/',null=True,blank=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.classname

class midcategory(models.Model):
    itmclass = models.ForeignKey(category,on_delete=models.SET_NULL,null=True)
    classname = models.CharField(max_length=50,null=True)
    midcategory_image = models.ImageField(upload_to='images/categories/',null=True,blank=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.itmclass)+" - "+str(self.classname)

class subcategory(models.Model):
    itmclass = models.ForeignKey(category,on_delete=models.SET_NULL,null=True, related_name="sub_category")
    itmmidclass = models.ForeignKey(midcategory,on_delete=models.SET_NULL,null=True)
    itmsubclass = models.CharField(max_length=50,null=True)
    classname = models.CharField(max_length=50,null=True)
    subcategory_image = models.ImageField(upload_to='images/categories/',null=True,blank=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.itmmidclass) + " - " + str(self.itmsubclass)

    @property
    def get_product_total(self):
        sub_product = products.objects.filter(itmsubclass = self.pk).aggregate(
            total_product = Sum('itmclass')
        )
        total_product = sub_product['total_product']
        if total_product:
            return total_product
        else:
            return 0

    

class products(models.Model):
    itmname = models.CharField(max_length=100, null=True)
    itmtitle = models.CharField(max_length=100,null=True)
    itmdesc = models.CharField(max_length=500, null=True)
    itm_old_price = models.IntegerField(null=True)
    itm_new_price = models.IntegerField(null=True)
    itmclass = models.ForeignKey(category,on_delete=models.SET_NULL,null = True)
    itmmidclass = models.ForeignKey(midcategory,default=None,on_delete=models.SET_NULL,null = True)
    itmsubclass = models.ForeignKey(subcategory,on_delete=models.SET_NULL,null = True)
    vendoraddedby = models.ForeignKey(customer,on_delete=models.SET_NULL,null = True)
    itm_isactive = models.BooleanField(default = True)
    sku_no = models.CharField(max_length=10,null=True,blank=True)
    itm_tags = models.CharField(max_length=10,null=True,blank=True)
    itm_barcode = models.CharField(max_length=10,null=True,blank=True)
    average_rating = models.FloatField(default=0.0,blank=True,null=True)
    total_review = models.IntegerField(default=0,blank=True,null=True)
    itm_datecreated = models.DateTimeField(auto_now_add=True)
    itm_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.itmname+str(self.id))

    @property
    def get_variants(self):
        product_variant = product_variants.objects.filter(product_id = self.id)
        return product_variant
    
    @property
    def get_sizes(self):
        product_size = product_sizes.objects.filter(product = self.id)
        return product_size
    

class product_images(models.Model):
    product_id = models.OneToOneField(products,on_delete=models.SET_NULL,null=True)
    image1 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image2 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image3 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image4 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image5 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    def __str__(self):
        return str(self.product_id)
    
    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            desired_width = 830
            desired_height = 620
            for field_name in ['image1', 'image2', 'image3', 'image4', 'image5']:
                image_field = getattr(self, field_name)
                if image_field:
                    print('Image path',image_field.path)
                    img = Image.open(image_field.path)
                    img_resized = ImageOps.pad(img, (desired_width, desired_height), color='white')
                    img_resized.save(image_field.path, quality=100)
        except Exception as e:
            print("Error converting image: ",e)

class product_variants(models.Model):
    product_id=models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    varient_name = models.CharField(max_length=10,null=True,blank=True)
    color_code = models.CharField(max_length=10,null=True,blank=True)
    quantity = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id) + str(self.varient_name)


class product_sizes(models.Model):
    SIZE_CHOICES = [
        ('sm', 'Extra Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
        ('xxl', 'Double Extra Large'),
    ]
    product = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    # product_variant = models.ForeignKey(product_variants,on_delete=models.SET_NULL,null=True,blank=True)
    product_price = models.IntegerField(null=True,blank=True)
    product_size = models.CharField(max_length=4, choices=SIZE_CHOICES, default=None)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)


class product_metas(models.Model):
    product_id = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    meta_link = models.CharField(max_length=50,null=True,blank=True)
    meta_title = models.CharField(max_length=50,null=True,blank=True)
    meta_description = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)
    
class favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='favourites',null=True,blank=True)
    def __str__(self):
        return str(self.user)
    
class favourite_items(models.Model):
    favourite_ins = models.ForeignKey(favourite,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    variant = models.ForeignKey(product_variants,on_delete=models.SET_NULL,null=True,blank=True)
    size = models.ForeignKey(product_sizes,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return str(self.favourite_ins)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='carts',null=True,blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + str(self.id)
    


class cartItems(models.Model):
    cart_ins = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    variant = models.ForeignKey(product_variants,on_delete=models.SET_NULL,null=True,blank=True)
    size = models.ForeignKey(product_sizes,on_delete=models.SET_NULL,null=True,blank=True)
    cart_count= models.IntegerField(default=0,blank=False,null=False)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.cart_ins) + str(self.id)

class orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='orders',null=True,blank=True)
    vendor_id = models.ForeignKey(store_details,on_delete=models.SET_NULL, null=True)
    orderdate = models.DateTimeField(auto_now_add=True)
    shippeddate = models.DateTimeField(null=True)
    deliverydate = models.DateTimeField(null=True)
    items = models.ManyToManyField(products)
    shipto = models.ForeignKey(address,on_delete=models.SET_NULL,null=True)
    cutomer_id = models.ForeignKey(customer,on_delete=models.SET_NULL, null=True)
    paymentid = models.CharField(max_length=50,null = False)
    order_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def order_total(self):
        total = 0
        for product in self.items.all():
            total += product.itm_new_price
        return total
    
class orderitems(models.Model):
    customer = models.ForeignKey(orders,on_delete=models.CASCADE,related_name='single_order',null=True,blank=True)
    order = models.ForeignKey(orders,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)
    

class order_invoices(models.Model):
    order_id = models.ForeignKey(orders,on_delete=models.SET_NULL,null=True)
    invoice_amount = models.IntegerField(null=True,blank=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    if_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)





class reviews(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(products, on_delete=models.SET_NULL,null=True)
    rating = models.IntegerField(null=True)
    review = models.CharField(max_length=100,null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review
    
class home_offers(models.Model):
    offer_title = models.CharField(max_length=50,null=False)
    offer_desc = models.CharField(max_length=100,null=False)
    offer_image = models.ImageField(upload_to='images/uploads/')
    offer_page = models.CharField(max_length=300,blank=True,null=True,default=None)
    date_created = models.DateTimeField(auto_now=True)

class category_offer(models.Model):
    offer_name = models.CharField(max_length=100,null=True,blank=True)
    offer_catgory = models.ForeignKey(category,on_delete=models.CASCADE,blank=False,null=False)
    offer_heading = models.CharField(max_length=40,default="",null=False,blank=False)
    offer_description = models.CharField(max_length=80,default="",null=False,blank=False)
    offer_image = models.ImageField(upload_to='images/offer_images/',null=True,blank=True)
    offer_url = models.CharField(max_length=200,blank=False,null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_upadated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.offer_name, self.offer_catgory.classname)
    

class discount_type(models.Model):
    offer_name = models.CharField(max_length =20,null=True,blank=False)
    date_created= models.DateTimeField(auto_now = True,blank=True)

    def __str__(self):
        return str(self.offer_name)

class discount(models.Model):
    offer = models.CharField(max_length =20,null=True,blank=False)
    offer_cat = models.ForeignKey(discount_type, on_delete=models.SET_NULL,null=True)
    if_on_category = models.ForeignKey(category,on_delete=models.SET_NULL,null=True,blank=True)
    if_on_product = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    discount_value = models.CharField(max_length=6,null=True,blank=True)
    vendor_by = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    date_created= models.DateTimeField(auto_now = True,blank=True)
    date_updated = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.offer)
    

class recently_viewed(models.Model):
    user = models.ForeignKey(buyer,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(products,on_delete=models.CASCADE,blank=True,null=True)
    frequency = models.CharField(max_length=20,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)+" - "+str(self.frequency)
    



