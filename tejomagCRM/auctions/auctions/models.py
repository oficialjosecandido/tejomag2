from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from taggit.managers import TaggableManager

# this is the model for users and it inherits AbstractUser
class User(AbstractUser):
    pass

# model for shopnow!
class Fixed(models.Model):
    seller = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.TextField()
    excerpt = models.CharField(max_length=100)
    price = models.IntegerField()
    os_choice = (
        ('Smartphones', 'Smartphones'), 
        ('Computadores', 'Computadores'), 
        ('Tablets', 'Tablets'), 
        ('Consolas', 'Consolas'), 
        ('Televisões', 'Televisões'),
        ('Drones', 'Drones'),
        ('Fotografia e Video', 'Fotografia e Video'),
        ('Outros', 'Outros')
    )
    category = models.CharField(max_length=64, blank=True, null=True, choices=os_choice)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    imagem1 = models.ImageField(upload_to = 'ofertas/', default = 'no-img.jpg')
    imagem2 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem3 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem4 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem5 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem6 = models.ImageField(upload_to = 'ofertas/', blank=True)
    shipping_cost= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}: por {self.seller} com o preço €{self.price} na data {self.created_at}:"

# model for listings
class Increase(models.Model):
    seller = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    description = models.TextField()
    excerpt = models.CharField(max_length=100)
    starting_bid = models.IntegerField()
    os_choice = (
        ('Smartphones', 'Smartphones'), 
        ('Computadores', 'Computadores'), 
        ('Tablets', 'Tablets'), 
        ('Consolas', 'Consolas'), 
        ('Televisões', 'Televisões'),
        ('Drones', 'Drones'),
        ('Fotografia e Video', 'Fotografia e Video'),
        ('Outros', 'Outros')
    )
    category = models.CharField(max_length=64, blank=True, null=True, choices=os_choice)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    imagem1 = models.ImageField(upload_to = 'ofertas/', default = 'no-img.jpg')
    imagem2 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem3 = models.ImageField(upload_to = 'ofertas/', blank=True)
    expert = models.IntegerField(default=0, blank=True)
    shipping_cost= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    deadline = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return f"{self.title}: por {self.seller} com uma bid de €{self.starting_bid} na data {self.created_at}:"

class Decrease(models.Model):  
    seller = models.CharField(max_length=300)
    title = models.CharField(max_length=30)
    description = models.TextField()
    excerpt = models.CharField(max_length=100)
    pbase = models.IntegerField()
    pmin = models.IntegerField()
    os_choice = (
        ('Smartphones', 'Smartphones'), 
        ('Computadores', 'Computadores'), 
        ('Tablets', 'Tablets'), 
        ('Consolas', 'Consolas'), 
        ('Televisões', 'Televisões'),
        ('Drones', 'Drones'),
        ('Fotografia e Video', 'Fotografia e Video'),
        ('Outros', 'Outros')
    )
    category = models.CharField(max_length=64, blank=True, null=True, choices=os_choice)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager() 
    imagem1 = models.ImageField(upload_to = 'ofertas/', default = 'no-img.jpg', blank=True)
    imagem2 = models.ImageField(upload_to = 'ofertas/', blank=True)
    imagem3 = models.ImageField(upload_to = 'ofertas/', blank=True)
    expert = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    deadline = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return f"{self.title}: por {self.seller} com uma base de €{self.pbase} na data {self.created_at}:"

# model for bids
class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user} colocou uma bid de {self.bid}."

#ofertas dos leilões invertidos
class oferta(models.Model):
    user = models.CharField(max_length=64)
    valor = models.IntegerField(null=True)
    listingid = models.IntegerField(null=True)
    title = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} colocou uma bid de {self.valor}."

# model for comments
class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    listingid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)




#vencedores dos leilões invertidos
class Vencedor(models.Model):
    vendedor = models.CharField(max_length=64)
    vencedor = models.CharField(max_length=64)
    listingid = models.IntegerField()
    image = models.ImageField()
    montante = models.IntegerField()
    titulo = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.titulo} por €{self.montante} reclamado por {self.vencedor}."

# model for watchlist
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    
    def __str__(self):
        return f"{self.user} está a observar o artigo {self.listingid}."

# model for ViewList
class ViewList(models.Model):
    user = models.CharField(max_length=64)
    decreaseid = models.IntegerField()
    
    def __str__(self):
        return f"{self.user} está a observar o artigo {self.decreaseid}."

# model to store the winners
class Winner(models.Model):
    owner = models.CharField(max_length=64)
    owner.email = models.EmailField()
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    image = models.ImageField()
    winprice = models.IntegerField()
    title = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.title} por €{self.winprice} reclamado por {self.winner}."
