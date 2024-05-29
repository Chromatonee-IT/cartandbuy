from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from store.models import *


class StaticSitemap(Sitemap):
    def items(self):
        return ['login','register','forgotpass','home','dashboard','orders','referal','address','my_reviews','my_favourites','cart']
    
    def location(self,item):
        return reverse(item)

    
class CategorySitemap(Sitemap):
    def items(self):
        return category.objects.all()
    

class SubcategorySitemap(Sitemap):
    def items(self):
        return midcategory.objects.all()

class ProductsSitemap(Sitemap):
    def items(self):
        return products.objects.all()[:100]
    
