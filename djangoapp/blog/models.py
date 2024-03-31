from django.db import models
from utils.rands import slugify_new

# Create your models here.

class Tag(models.Model):
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=50
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        
        return super().save(*args,*kwargs) 


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name= models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=50
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        
        return super().save(*args,*kwargs) 