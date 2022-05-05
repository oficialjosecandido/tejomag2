from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from auctions.serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from . import forms
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.conf import settings
from django.views.generic import View
from auctions.forms import ContactForm

import datetime
import json


""" @csrf_exempt
def banners5Api(request, id=0):
    banners = Banner.objects.order_by('-created_at')[:4]
    banners_serializer = BannersSerializer(banners, many=True)
    return JsonResponse(banners_serializer.data, safe=False) """


class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'auctions/create2News.html')

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect('contact')
        return render(request, 'auctions/create2News.html', {'form': form})


def newsAPI(request, id=0):
    news = News.objects.order_by('-date')[:4]
    news_serializer = FlashNewsSerializer(news, many=True)
    return JsonResponse(news_serializer.data, safe=False) 

def articlesSprintAPI(request, id=0):
    articles = Article.objects.filter(sprint = True)
    articles_serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(articles_serializer.data, safe=False) 

def newsDetailsAPI(slug):
    news = News.objects.filter(slug=slug)
    news_serializer = FlashNewsSerializer(news, many=True)
    return JsonResponse(news_serializer.data, safe=False) 

# this is the default view
def index(request):

    destaques = Listing.objects.filter(featured = True)
    
    context = {
        'destaques': destaques,
    }
    
    return render(request, "auctions/index.html", context)

# this is the mocks view
def mocks(request):    
    return render(request, "auctions/mocks.html")

# this is the view for login
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "auctions/index.html", {
                "message": "Sessão iniciada com sucesso",
                "msg_type": "success"
            })
        # if not authenticated
        else:
            return render(request, "auctions/llogin.html", {
                "message": "Username ou Palavra Passe Inválidos",
                "msg_type": "danger"
            })
    # if GET request
    else:
        return render(request, "auctions/llogin.html")

# view for logging out
def logout_view(request):
    logout(request)
    return render(request, "auctions/index.html", {
        "message": "Sessão terminada com sucesso",
        "msg_type": "danger"
    })

# view for registering
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "As palavras-passe não são iguais.",
                "msg_type": "danger"
            })
        if not username:
            return render(request, "auctions/register.html", {
                "message": "Por favor introduza um username.",
                "msg_type": "danger"
            }) 

        if not email:
            return render(request, "auctions/register.html", {
                "message": "Por favor introduza um email.",
                "msg_type": "danger"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()        
            send_mail('BemVindo à TEJOmag', 
                    'Serve este email para confirmar o seu registo na nossa plataforma de backoffice', 
                    settings.EMAIL_HOST_USER, 
                    [email], 
                    fail_silently=False)
            return render(request, "auctions/index.html", {
                "message": "Username ou Email já estão registados.",
                "msg_type": "success"
            })

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username ou Email já estão registados.",
                "msg_type": "danger"
            })
        login(request, user)
        return render(request, "auctions/index.html")

    # if GET request
    else:
        return render(request, "auctions/register.html")



# view for dashboard
@login_required(login_url='/llogin')
def dashboard(request):
    winners = Winner.objects.filter(winner=request.user.username)
    mensagem = Notification.objects.filter(receiver=request.user.username)
    contador = mensagem.count()
    #image = Listing.objects.filter(image=request.imagem1)
    # checking for watchlist
    lst = Watchlist.objects.filter(user=request.user.username)
    # list of products available in WinnerModel
    present = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Listing.objects.get(id=item.listingid)
            prodlst.append(product)
    print(prodlst)
    return render(request, "auctions/dashboard.html", {
        "product_list": prodlst,
        "present": present,
        "products": winners,
        'mensagem': mensagem,
        'contador': contador,
    })


# backoffice create News
@login_required(login_url='/llogin')
def createNews(request):    
    form = newsForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        send_mail('TEJOmag | flashNews para aprovação', 
                    'Serve este email para confirmar que ' + request.user.username + ' criou uma flashNews. Obrigado', 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email, 'geral@tejomag.pt'], 
                    fail_silently=False)
        return render(request, 'auctions/index.html', {"message": "O seu post foi enviado para aprovação. Obrigado"})
    
    
    return render(request, 'auctions/createNews.html', {
        "form": form,
    })

@login_required(login_url='/llogin')
def createArticle(request):    
    form = articleForm(request.POST)
    if form.is_valid():
        form.save()
        send_mail('TEJOmag | Novo Artigo para aprovação', 
                    'Serve este email para confirmar que ' + request.user.username + ' criou um novo Artigo. Obrigado', 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email, 'geral@tejomag.pt'], 
                    fail_silently=False)
        return render(request, 'auctions/createArticle.html', {"message": "O seu artigo foi enviado para aprovação. Obrigado"})
    
    
    return render(request, 'auctions/createArticle.html', {
        "form": form,
    })



# frontEnd news details page
def newsDetails(request, slug):
    news = News.objects.filter(slug=slug)
    if news :
        news[0].views += 1
        news_serializer = FlashNewsSerializer(news, many=True)
        return JsonResponse(news_serializer.data, safe=False)
    return render(request, 'auctions/newsDetails.html', {'news':news})

# backup News Details Page
def BOnewsDetails(request, slug):
    news = News.objects.filter(slug=slug)[0]
    return render(request, 'auctions/newsDetails.html', {'news':news})


# frontEnd news details page
def articleDetails(request, slug):
    article = Article.objects.filter(slug=slug)
    if article :
        article[0].views += 1
        article_serializer = ArticleSerializer(article, many=True)
        return JsonResponse(article_serializer.data, safe=False)
    return render(request, 'auctions/articleDetails.html', {'article':article})

# backup News Details Page
def BOarticleDetails(request, slug):
    article = Article.objects.filter(slug=slug)[0]
    return render(request, 'auctions/articleDetails.html', {'article':article})



def search(request): 
    template = 'auctions/resultados.html'
    query = request.GET.get('q')
    if query:
        results = Listing.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:  
        results = Listing.objects.all()

    paginator = Paginator(results, 30)
    page = request.GET.get('page')
    try: 
        results = paginator.page(page)
    except PageNotAnInteger:  
        results = paginator.page(1)
    except EmptyPage: 
        results = paginator.page(paginator.num_pages())

    index = results.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]


   # pages = Paginator(request, results)

    #context = {
    #    'items': pages[0],
    #    'page_range': pages[1],
    #}

    return render(request, template, {'results': results})

def contact(request): 
    template = 'auctions/contact.html'


    if request.method == 'POST':
        name = request.POST['message_name']
        email = request.POST['message_email']
        messagem = request.POST['message']

        send_mail(

            "Contacto de: " + name,
            email +" escreveu: " + messagem,
            email,
            ['geral@tejomag.pt', 'josevcandido@gmail.com'],
            fail_silently=False
        )
        
        return render(request, template, {'name': name, "message": 'Mensagem enviada.',
        "msg_type": 'success'})
    else:  
        return render(request, template)

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    vendas = Listing.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'vendas': vendas
    }
    
    return render(request, 'auctions/tags.html', context)
