
import random
import os

from django.db import models

# Note: each time models file is changed, the following must be done
# also:
# 1-makemigrations 2- migrate.

def get_file_name_ext(filepath):
    base_name   = os.path.basename(filepath)
    name, ext   = os.path.splitext(base_name)

    return name, ext


def  upload_image_path(instance, filename):
    print(instance)
    print(filename)

    new_filename    = random.randint(0,100000000)
    name, ext       = get_file_name_ext(filename)
    final_filename  = '{new_filename}{ext}'

    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename,
                                                        final_filename=final_filename)
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)
    
    def featured(self):
        return self.filter(featured = True, active = True)

class ProductManager(models.Manager):


    def all(self):
        return self.get_queryset().active()

    def det_queryset(self):
        return ProductQuerySet(self.model, self._db)

    def featured(self):
        return self.get_queryset().featured

    def get_by_id(self,id):

        qs = self.get_queryset().filter(id=id)# == Product.objects == self.get_queryset()

        if qs.count()==1:

            return qs.first()

        return None

class Product(models.Model):
    title       =  models.CharField(max_length= 120)

    slug        = models.SlugField(blank = True, null = True)

    description = models.TextField()# Text fields length is bound by the database type and support.

    price       = models.DecimalField(decimal_places=2, max_digits=20, default=39.99 )

    image       = models.ImageField(upload_to=upload_image_path, null=True,blank=True)

    objects     = ProductManager()

    featured    = models.BooleanField(default=False)

    active    = models.BooleanField(default=True)

    def __str__(self):
        return self.title































