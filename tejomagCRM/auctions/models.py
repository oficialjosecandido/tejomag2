from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from django.utils.text import slugify


# this is the model for users and it inherits AbstractUser
class User(AbstractUser):
    role = models.CharField(max_length=100, null=True, blank=True)

#model for News
class News(models.Model):
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    tags = TaggableManager() 
    slug = models.SlugField(unique=True, max_length=100)
    os_choice = (
        ('Economia', 'Economia'), 
        ('Politica', 'Politica'), 
        ('Mundo', 'Mundo'), 
        ('Desporto', 'Desporto'), 
        ('Justiça', 'Justiça'),
        ('Lifestyle', 'Lifestyle'),
        ('Tecnologia', 'Tecnologia'),
        ('Ciência', 'Ciência')
    )
    category = models.CharField(max_length=64, choices=os_choice)
    stata = (
        ('Em atualização', 'Em atualização'),
        ('Fontes não verificadas', 'Fontes não verificadas'),
        ('Verificado', 'Verificado'),
        ('Fake News', 'Fake News')
    )
    status = models.CharField(max_length=64, choices=stata)

    title = models.CharField(max_length=30)
    excerpt = models.CharField(max_length=500)
    p1 = models.TextField()
    p2 = models.TextField(null=True, blank=True)
    p3 = models.TextField(null=True, blank=True)
    p4 = models.TextField(null=True, blank=True)
    p5 = models.TextField(null=True, blank=True)
    image1_link = models.CharField(max_length=500, null=True, blank=True)
    image2_link = models.CharField(max_length=500, null=True, blank=True)
    image3_link = models.CharField(max_length=500, null=True, blank=True)
    image4_link = models.CharField(max_length=500, null=True, blank=True)
    image5_link = models.CharField(max_length=500, null=True, blank=True)
    image6_link = models.CharField(max_length=500, null=True, blank=True)
    image7_link = models.CharField(max_length=500, null=True, blank=True)
    image8_link = models.CharField(max_length=500, null=True, blank=True)
    image9_link = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs): 
        self.slug=slugify(self.excerpt)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}: por {self.author} na data {self.date} e com {self.views} views"


#model for Articles
class Article(models.Model):
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=100)
    os_choice = (
        ('Economia', 'Economia'), 
        ('Politica', 'Politica'), 
        ('Mundo', 'Mundo'), 
        ('Desporto', 'Desporto'), 
        ('Justiça', 'Justiça'),
        ('Lifestyle', 'Lifestyle'),
        ('Tecnologia', 'Tecnologia'),
        ('Ciência', 'Ciência')
    )
    category = models.CharField(max_length=64, choices=os_choice)
    stata = (
        ('Entrevista', 'Entrevista'),
        ('Reportagem', 'Reportagem'),
        ('Investigação', 'Investigação'),
        ('Opinião', 'Opinião')
    )
    type = models.CharField(max_length=64, choices=stata)
    featured = models.BooleanField(default=False, null=True, blank=True)
    sprint = models.BooleanField(default=False, blank=True, null=True)

    title = models.CharField(max_length=30, null=True, blank=True)
    excerpt = models.CharField(max_length=500, null=True, blank=True)
    p1 = models.TextField(null=True, blank=True)
    p2 = models.TextField(null=True, blank=True)
    p3 = models.TextField(null=True, blank=True)
    p4 = models.TextField(null=True, blank=True)
    p5 = models.TextField(null=True, blank=True)
    author_username = models.CharField(max_length=500, null=True, blank=True)
    image1_link = models.CharField(max_length=500, null=True, blank=True)
    image2_link = models.CharField(max_length=500, null=True, blank=True)
    image3_link = models.CharField(max_length=500, null=True, blank=True)
    image4_link = models.CharField(max_length=500, null=True, blank=True)
    image5_link = models.CharField(max_length=500, null=True, blank=True)
    image6_link = models.CharField(max_length=500, null=True, blank=True)
    image7_link = models.CharField(max_length=500, null=True, blank=True)
    image8_link = models.CharField(max_length=500, null=True, blank=True)
    image9_link = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs): 
        self.slug=slugify(self.excerpt)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}: por {self.author} na data {self.date} e com {self.views} views"



# model for listings
class Listing(models.Model):
    seller = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.TextField()
    excerpt = models.CharField(max_length=100)
    starting_bid = models.IntegerField()
    os_choice = (
        ('Smartphones', 'Smartphones'), 
        ('Computadores', 'Computadores'), 
        ('Gadgets', 'Gadgets'), 
        ('Consolas', 'Consolas'), 
        ('Bicicletas Motorizadas', 'Bicicletas Motorizadas'),
        ('Drones', 'Drones'),
        ('Fotografia e Video', 'Fotografia e Video'),
        ('Outros', 'Outros')
    )
    category = models.CharField(max_length=64, choices=os_choice)
    tags = TaggableManager() 
    slug = models.SlugField(unique=True, max_length=100)
    imagem1 = models.ImageField(upload_to = 'ofertas/', default = 'no-img.jpg')
    imagem2 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem3 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem4 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem5 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem6 = models.ImageField(upload_to = 'ofertas/', blank=True)
    expert = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    deadline = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}: por {self.seller} com uma bid de €{self.starting_bid} na data {self.created_at}:"

