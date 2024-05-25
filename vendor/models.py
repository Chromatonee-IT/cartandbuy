from django.db import models
from django.contrib.auth.models import User
from store.models import *


class store_details(models.Model):
    store_vendor = models.OneToOneField(User, on_delete=models.SET_NULL,null = True)
    store_name = models.CharField(max_length=50)
    store_email = models.CharField(max_length=100,null=True,blank=True)
    store_logo = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None,null=True,blank = True)
    abline1 = models.CharField(max_length=200,blank=True, null=True)
    abline2 = models.CharField(max_length=200, blank=True,null=True)
    abline3 = models.CharField(max_length=200,blank=True ,null=True)
    city = models.CharField(max_length=200,blank=True, null=True)
    district = models.CharField(max_length=200, blank=True,null=True)
    state = models.CharField(max_length=200, blank=True,null=True)
    zip = models.IntegerField(null=False,default=000000)
    store_facebook = models.CharField(max_length=100,null=True,blank=True)
    store_instagram = models.CharField(max_length=100,null=True,blank=True)
    store_twitter = models.CharField(max_length=100,null=True,blank=True)
    store_date_created = models.DateTimeField(auto_now=True)
    store_date_updated = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.store_name)

class store_document(models.Model):
    store_vendor = models.OneToOneField(User, on_delete=models.SET_NULL,null = True)
    adhar_card = models.ImageField(upload_to='kyc/',null=False,blank = False)
    pan_card = models.ImageField(upload_to='kyc/',null=False,blank = False)
    cancel_check = models.ImageField(upload_to='kyc/',null=False,blank = False)
    bank_micr = models.CharField(max_length=9,null=False,blank = False)
    trade_lisence = models.ImageField(upload_to='kyc/',null=True,blank = True)
    gst_certificate = models.ImageField(upload_to='kyc/',null=True,blank = True)
    gst_no = models.CharField(max_length=100,null=True,blank = True)

    def __str__(self):
        return str(self.store_vendor)
