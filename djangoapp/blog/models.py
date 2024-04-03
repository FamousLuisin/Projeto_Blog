from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.imagens import resize_image
from django_summernote.models import AbstractAttachment

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
        
        return super().save(*args,**kwargs) 
    
    def __str__(self):
        return self.name


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
        
        return super().save(*args,**kwargs) 
    
    def __str__(self):
        return self.name
    

class Page(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=50
    )
    is_publishe = models.BooleanField(
        default=False, 
        help_text='Caso queira mostrar a pagina deve ativar'
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        
        return super().save(*args,**kwargs) 
    
    def __str__(self):
        return self.title
    

class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65)
    
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=50
    )

    objects = PostManager()
    
    excerpt = models.CharField(max_length=250)
    is_published = models.BooleanField(
        default=False, 
        help_text='Caso queira mostrar a pagina deve marcar'
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Exibir capa de imagem no conteudo do post?'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank = True, null=True,
        related_name='post_created_by'
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank = True, null=True,
        related_name='post_updated_by'
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save 
    
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)
        
        return super_save 