from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
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

import datetime
import json


""" @csrf_exempt
def banners5Api(request, id=0):
    banners = Banner.objects.order_by('-created_at')[:4]
    banners_serializer = BannersSerializer(banners, many=True)
    return JsonResponse(banners_serializer.data, safe=False) """


def newsAPI(request, id=0):
    news = News.objects.order_by('-date')[:4]
    news_serializer = NewsSerializer(news, many=True)
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
    print('passei aqui.....')
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


@login_required(login_url='/llogin')
def vencidos(request): 

    # Filtrar os vencedores de Leilões
    winners = Winner.objects.filter(winner=request.user.username)
    total_winners = winners.count()

    context = {
        'winners': winners,
        'total_winners': total_winners,
    } 
    
    return render(request, 'auctions/vencidos.html', context)


@login_required(login_url='/llogin')
def publicados(request):  
    
    # Filtrar as ofertas colocadas
    sellers = Listing.objects.filter(seller=request.user.username)
    total_sellers = sellers.count()

    context = {
        "total_sellers": total_sellers,
        "sellers": sellers,
    }

    return render(request, 'auctions/publicados.html', context)

@login_required(login_url='/llogin')
def dwatchlist(request):

    lst = Watchlist.objects.filter(user=request.user.username)
    present = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Listing.objects.get(id=item.listingid)
            prodlst.append(product)
    print(prodlst)

    return render(request, "auctions/watchlist.html", {
        "present": present,
        "products": prodlst
    })

# History of all my bids
@login_required(login_url='/login')
def dhistorico(request):
    mensagem = Notification.objects.filter(receiver=request.user.username)
    contador = mensagem.count()
    lista = Bid.objects.filter(user=request.user.username).order_by("-listingid")

    return render(request, "auctions/dhistorico.html", {        
        'lista': lista,
        'mensagem': mensagem,
        'contador': contador,
    })


# view for showing all Listings
def activelisting(request):
    # list of products available
    products = Listing.objects.order_by('-created_at')
    total = Listing.objects.count()

    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
        
    return render(request, "auctions/activelisting.html", {
        "products": products,
        "total": total,
        "empty": empty
    })

# view for showing all Listings
def winners(request):
    # list of products available
    products = Winner.objects.all()
    total = Winner.objects.count()

    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
        
    return render(request, "auctions/winners.html", {
        "products": products,
        "total": total,
        "empty": empty
    })


# view to display individual listing
@login_required(login_url='/llogin')
def viewlisting(request, product_id):
    # if the user submits his bid
    loves = Watchlist.objects.filter(
            listingid=product_id).count()
    comments = Comment.objects.filter(listingid=product_id)

    history = Bid.objects.filter(listingid=product_id).order_by('-created_at')
    lasthistory = Bid.objects.filter(listingid=product_id).order_by('-created_at')[:5]

    if request.method == "POST":
        item = Listing.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))

        
        # checking if the newbid is greater than or equal to current bid
        if item.starting_bid >= newbid:
            # saving the bid in Bid model
            obj = Bid()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = product_id
            obj.bid = newbid
            obj.save()
            send_mail('2Mão | Licitação Registada com Sucesso', 
                    'Serve este email para confirmar a sua licitação', 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email], 
                    fail_silently=False)
            return render(request, "auctions/activelisting.html", {
                "message": "A sua oferta foi aceite.",
                "msg_type": "success",
                'history': history,
                'lasthistory': lasthistory,
                "comments": comments
            })
        # if bid is greater then updating in Listings table
        else:
            item.starting_bid = newbid
            item.save()
            # saving the bid in Bid model
            
            obj = Bid()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = product_id
            obj.bid = newbid
            obj.save()
            send_mail('2Mão | Licitação Registada com Sucesso', 
                    'Serve este email para confirmar a sua licitação', 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email], 
                    fail_silently=False)


            return render(request, "auctions/activelisting.html", {
                "message": "A sua oferta foi aceite.",
                "msg_type": "success",
                'history': history,
                'lasthistory': lasthistory,
                "comments": comments
            })

            
    # accessing individual listing GET
    else:
        product = Listing.objects.get(id=product_id)
        bids = Listing.objects.filter(id=product_id).count()

        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        loves = added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "bids":bids,
            "loves": loves,
            "added": added,
            'history': history,
            'lasthistory': lasthistory,
            "comments": comments
        })

# View to add or remove products to watchlists
@login_required(login_url='/llogin')
def addtowatchlist(request, product_id):
    loves = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
    obj = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=product_id)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "loves": loves,
            "comments": comments
        })
    else:
        # if it not present then the user wants to add it to watchlist
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        # returning the updated content
        product = Listing.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })

# view for comments
@login_required(login_url='/llogin')
def addcomment(request, product_id):
    obj = Comment()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listingid = product_id
    obj.save()
    # returning the updated content
    print("displaying comments")
    comments = Comment.objects.filter(listingid=product_id)
    product = Listing.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })

# view to display all the active listings in that category
@login_required(login_url='/llogin')
def category(request, categ):
    # retieving all the products that fall into this category
    categ_products = Listing.objects.filter(category=categ)
    empty = False
    if len(categ_products) == 0:
        empty = True
    return render(request, "auctions/category.html", {
        "categ": categ,
        "empty": empty,
        "products": categ_products
    })

# view when the user wants to close the bid
@login_required(login_url='/llogin')
def closebid(request, product_id):
    winobj = Winner()

    listobj = Listing.objects.get(id=product_id)
    obj = get_object_or_404(Bid, listingid=product_id)
    if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bidobj = Bid.objects.get(listingid=product_id)
        winobj.owner = request.user.username
        winobj.email = request.user.email
        winobj.winner = bidobj.user
        winobj.listingid = product_id
        winobj.winprice = bidobj.bid
        winobj.title = bidobj.title
        winobj.save()
        message = "Leilão Terminado. Pode entrar em contacto com o vencedor para o seu email " + winobj.winner
        msg_type = "success"


        if winobj:
            name =  winobj.winner
            email =  winobj.email
            messagem = 'A sua oferta foi licitada com sucesso. Por favor responda a este email com os seus contactos para entrar em contacto consigo e tratarmos do pagamento e entrega. Obrigado'

        send_mail(

            "Parabéns. O seu leilão encontrou um vencedor: " + name,
            email +" escreveu: " + messagem,
            email,
            ['mh.josevicente@gmail.com', 'josevcandido@gmail.com'],
            fail_silently=False
        )
        # removing from Bid
        bidobj.delete()
        
    
    # removing from watchlist
    if Watchlist.objects.filter(listingid=product_id):
        watchobj = Watchlist.objects.filter(listingid=product_id)
        watchobj.delete()
    # removing from Comment
    if Comment.objects.filter(listingid=product_id):
        commentobj = Comment.objects.filter(listingid=product_id)
        commentobj.delete()
    # removing from Listing
    listobj.delete()
    # retrieving the new products list after adding and displaying
    # list of products available in WinnerModel
    winners = Winner.objects.all()
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type
    })

# view to see closed listings
@login_required(login_url='/llogin')
def closedlisting(request):
    # list of products available in WinnerModel
    winners = Winner.objects.all()
    item = Listing.objects.all()
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        "items": item
    })

# view to create a lisiting
@login_required(login_url='/llogin')
def anunciar(request):
    
    products = Listing.objects.order_by('-created_at')

    form = Anunciar(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        send_mail('2Mão | Leilão Criado com Sucesso', 
                    'Serve este email para confirmar que o seu leilão foi criado com sucesso', 
                    settings.EMAIL_HOST_USER, 
                    [request.user.email], 
                    fail_silently=False)
        return render(request, 'auctions/activelisting.html', {"message": "O seu Leilão foi publicado por 30 dias. Obrigado", "products": products})
    
    
    return render(request, 'auctions/anunciar.html', {
        "form": form,
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

# frontEnd news details page
def newsDetails(request, slug):
    news = News.objects.filter(slug=slug)
    if news :
        news[0].views += 1
        print(news)
        news_serializer = FlashNewsSerializer(news, many=True)
        return JsonResponse(news_serializer.data, safe=False)
    return render(request, 'auctions/newsDetails.html', {'news':news})

# backup News Details Page
def BOnewsDetails(request, slug):
    news = News.objects.filter(slug=slug)[0]
    return render(request, 'auctions/newsDetails.html', {'news':news})

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
            ['mh.josevicente@gmail.com', 'josevcandido@gmail.com'],
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

def tc(request):

    return render(request, 'auctions/tc.html')

def pp(request):
    
    return render(request, 'auctions/pp.html')



def categ_smartphones(request):  

    increases = Listing.objects.order_by('-created_at') 
    context = {
        'increases': increases,
    }
    return render(request,"auctions/smartphones.html", context)

def categ_computadores(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/computadores.html', context)

def categ_consolas(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/consolas.html', context)

def categ_gadgets(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/gadgets.html', context)

def categ_video(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/video.html', context)

def categ_televisores(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/televisores.html', context)

def categ_drones(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }

    return render(request, 'auctions/drones.html', context)

def categ_outros(request):  
    
    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/outros.html', context)


def categ_video(request):  

    increases = Listing.objects.order_by('-created_at')
    context = {
        'increases': increases,
    }
    return render(request, 'auctions/video.html', context)