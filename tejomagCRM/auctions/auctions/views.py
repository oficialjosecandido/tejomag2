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


# this is the default view
def index(request):

    destaques = Increase.objects.filter(featured = True)
    invertos = Decrease.objects.filter(featured = True)

    context = {
        'destaques': destaques,
        'invertos': invertos
    }
    
    return render(request, "auctions/index.html", context)

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
            return render(request, "auctions/login.html", {
                "message": "Username ou Palavra Passe Inválidos",
                "msg_type": "danger"
            })
    # if GET request
    else:
        return render(request, "auctions/login.html")

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
            send_mail('BemVindo ao 2Mão', 
                    'Serve este email para confirmar o seu registo na nossa plataforma', 
                    settings.EMAIL_HOST_USER, 
                    [email], 
                    fail_silently=False)
            return HttpResponseRedirect(reverse("index"))

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username ou Email já estão registados.",
                "msg_type": "danger"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # if GET request
    else:
        return render(request, "auctions/register.html")

# view for dashboard
@login_required(login_url='/login')
def dashboard(request):
    

    lista = Bid.objects.filter(user=request.user.username)
    invertos = oferta.objects.filter(user=request.user.username)

    # Filtrar os vencedores de Leilões Invertidos
    dcompras = Vencedor.objects.filter(vencedor=request.user.username)
    total_vencedores = dcompras.count()

    return render(request, "auctions/dashboard.html", {
        
        'lista': lista,
        'invertos': invertos,
        #"amount": amount,
        "dcompras": dcompras
    })

# view for dashboard
@login_required(login_url='/login')
def dhistorico(request):
    
    lista = Bid.objects.filter(user=request.user.username).order_by("-listingid")
    invertos = oferta.objects.filter(user=request.user.username).order_by("-listingid")

    return render(request, "auctions/dhistorico.html", {        
        'lista': lista,
        'invertos': invertos,
    })

@login_required(login_url='/login')
def vencidos(request): 

    # Filtrar os vencedores de Leilões Normais
    winners = Winner.objects.filter(winner=request.user.username)
    total_winners = winners.count()

    # Filtrar os vencedores de Leilões Invertidos
    vencedores = Vencedor.objects.filter(vencedor=request.user.username)
    total_vencedores = winners.count()

    context = {
        'winners': winners,
        'total_winners': total_winners,
        'vencedores': vencedores,
        'total_vencedores': total_vencedores
    } 
    
    return render(request, 'auctions/vencidos.html', context)

@login_required(login_url='/login')
def publicados(request):  
    
    # Filtrar as ofertas colocadas
    sellers = Increase.objects.filter(seller=request.user.username)
    total_sellers = sellers.count()

    # Filtrar as Leilões Invertidos
    vendedores = Decrease.objects.filter(seller=request.user.username)
    total_vendedores = vendedores.count()

    context = {
        "total_sellers": total_sellers,
        "total_vendedores": total_vendedores,
        "sellers": sellers,
        "vendedores": vendedores
    }

    return render(request, 'auctions/publicados.html', context)

@login_required(login_url='/login')
def LikeView(request, pk):
    post = get_object_or_404(Increase, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('viewlisting', args=[str(pk)]))


@login_required(login_url='/login')
def dwatchlist(request):

    lst = Watchlist.objects.filter(user=request.user.username)
    present = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Increase.objects.get(id=item.listingid)
            prodlst.append(product)
    print(prodlst)

    return render(request, "auctions/watchlist.html", {
        "present": present,
        "products": prodlst
    })


@login_required(login_url='/login')
def dviewlist(request):

    lst = ViewList.objects.filter(user=request.user.username)
    # list of products available in WinnerModel
    present = False
    prodlst = []
    i = 0
    if lst:
        present = True
        for item in lst:
            product = Decrease.objects.get(id=item.decreaseid)
            prodlst.append(product)
    print(prodlst)

    context = {
        'products': prodlst,
        "present": present,
        'lst': lst,
    }

    return render(request, 'auctions/viewlist.html', context)



# view for showing the INCREASES ALL
def activelisting(request):
    # list of products available
    products = Increase.objects.order_by('-created_at')
    total = Increase.objects.count()
    common_tags = Increase.tags.most_common()[:3]
    loves = Watchlist.objects.all().count()

    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
        
    return render(request, "auctions/activelisting.html", {
        "products": products,
        'loves': loves,
        "total": total,
        "common_tags": common_tags,
        "empty": empty
    })

# view for showing the DECREASES ALL
def invertidos(request):
    # list of products available
    products = Decrease.objects.order_by('-created_at')
    total = Decrease.objects.count()
    common_tags = Decrease.tags.most_common()[:5]
       
    # checking if there are any products
    empty = False
    if len(products) == 0:
        empty = True
        
    return render(request, "auctions/invertidos.html", {
        "products": products,
        "total": total,
        "common_tags": common_tags,
        "empty": empty
    })

# view for showing the aFIXED ALL
def fixed(request):
    vendas = Fixed.objects.order_by("-created_at")
    common_tags = Fixed.tags.most_common()[:5]

    context = {
        'vendas': vendas,
        'common_tags': common_tags,
    }
    return render(request, 'auctions/fixed.html', context)

# view to display individual listing
def artigo(request, product_id):
    # if the user submits his bid
    #loves = Watchlist.objects.filter(
            #listingid=product_id, user=request.user.username).count()
    ofertas = oferta.objects.filter(listingid=product_id)
    if request.method == "POST":
        product = Decrease.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))
        bids = Decrease.objects.filter(id=product_id).count()

        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)

        return render(request, "auctions/artigo.html", {
            "product": product,
            "bids":bids,
            "added": added,
            "ofertas": ofertas
        })  
        
    # accessing individual listing GET
    else:
        product = Decrease.objects.get(id=product_id)
        bids = Decrease.objects.filter(id=product_id).count()

        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        
        return render(request, "auctions/artigo.html", {
            "product": product,
            "bids":bids,
            "added": added,
            "ofertas": ofertas
        })

# view to display individual listing
def viewlisting(request, product_id):
    # if the user submits his bid
    loves = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
    comments = Comment.objects.filter(listingid=product_id)

    history = Bid.objects.filter(listingid=product_id)

    if request.method == "POST":
        item = Increase.objects.get(id=product_id)
        newbid = int(request.POST.get('newbid'))

        
        # checking if the newbid is greater than or equal to current bid
        if item.starting_bid >= newbid:
            product = Increase.objects.get(id=product_id)
            loves = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
            bids = Increase.objects.filter(id=product_id).count()

            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "bids": bids,
                "message": "A sua oferta deve ser superior à actual licitação.",
                "msg_type": "danger",
                'history': history,
                "comments": comments
            })
        # if bid is greater then updating in Listings table
        else:
            item.starting_bid = newbid
            item.save()
            # saving the bid in Bid model
            bidobj = Bid.objects.filter(listingid=product_id)
            #if bidobj:
            #    bidobj.delete()
            
                
            obj = Bid()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = product_id
            obj.bid = newbid
            obj.save()
            product = Increase.objects.get(id=product_id)
            loves = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
            bids = Increase.objects.filter(id=product_id).count()
            ofertas = bidobj.count()

            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "ofertas": ofertas,
                "bids": bids,
                "loves": loves,
                "message": "A sua oferta foi aceite.",
                "msg_type": "success",
                'history': history,
                "comments": comments
            })

            
    # accessing individual listing GET
    else:
        product = Increase.objects.get(id=product_id)
        bids = Increase.objects.filter(id=product_id).count()

        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        loves = added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username).count()
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "bids":bids,
            "loves": loves,
            "added": added,
            "comments": comments
        })

# view for comments
@login_required(login_url='/login')
def colocaroferta(request, product_id):
    
    obj = oferta()
    obj.valor = request.POST.get("valor")
    obj.user = request.user.username
    obj.listingid = product_id
    products = Decrease.objects.filter(id=product_id)
    obj.save()    
    
    # returning the updated content
    print("displaying comments")
    dado = oferta.objects.filter(listingid=product_id).order_by("-timestamp")
    product = Decrease.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "auctions/artigo.html", {
        "product": product,
        "added": added,
        "ofertas": dado,
        "message": "Oferta Aceite. Obrigado",
        "msg_type": "success",
    })

# view to display all the categories
def categories(request):
    return render(request, "auctions/categories.html")


# View to add or remove products to watchlists
@login_required(login_url='/login')
def addtowatchlist(request, product_id):

    obj = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = Increase.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)

        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "message": "Removido da sua Watchlist",
            "msg_type": "danger",
        })
    else:
        # if it not present then the user wants to add it to watchlist
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = product_id
        obj.save()
        # returning the updated content
        product = Increase.objects.get(id=product_id)
        added = Watchlist.objects.filter(
            listingid=product_id, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "message": "Adicionado à sua Watchlist",
            "msg_type": "success",
        })

# View to add or remove products to watchlists
@login_required(login_url='/login')
def addtoview(request, product_id):
    
    obj = ViewList.objects.filter(
    decreaseid=product_id, user=request.user.username)
    # checking if it is already added to the watchlist
    if obj:
        # if its already there then user wants to remove it from watchlist
        obj.delete()
        # returning the updated content
        product = Decrease.objects.get(id=product_id)
        added = ViewList.objects.filter(
            decreaseid=product_id, user=request.user.username)
        return render(request, "auctions/artigo.html", {
            "product": product,
            "added": added,
        })
    else:
        # if it not present then the user wants to add it to watchlist
        obj = ViewList()
        obj.user = request.user.username
        obj.decreaseid = product_id
        obj.save()
        # returning the updated content
        product = Decrease.objects.get(id=product_id)
        added = ViewList.objects.filter(
            decreaseid=product_id, user=request.user.username)
        return render(request, "auctions/artigo.html", {
            "product": product,
            "added": added,
        })

# view for comments
@login_required(login_url='/login')
def addcomment(request, product_id):
    obj = Comment()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listingid = product_id
    obj.save()
    # returning the updated content
    print("displaying comments")
    comments = Comment.objects.filter(listingid=product_id)
    product = Increase.objects.get(id=product_id)
    added = Watchlist.objects.filter(
        listingid=product_id, user=request.user.username)
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })

# view when the user wants to close the bid
@login_required(login_url='/login')
def closebid(request, product_id):
    winobj = Winner()

    listobj = Increase.objects.get(id=product_id)
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
def closedlisting(request):
    # list of products available in WinnerModel
    winners = Winner.objects.all()
    terminados = Increase.objects.filter(terminado = True)
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closedlisting.html", {
        "products": winners,
        "empty": empty,
        "terminados": terminados,
    })

# view to see closed listings
def terminados(request):
    
    products = Increase.objects.filter(terminado = True)
    total = products.count()
    
    return render(request, "auctions/terminados.html", {
        "products": products,
        'total': total,
    })

# view to see closed listings
def vencedores(request):
    # list of products available in WinnerModel
    vencedores = Vencedor.objects.all()
    terminados = Decrease.objects.filter(terminado = True)
    # checking if there are any products
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/vencedores.html", {
        "products": vencedores,
        "empty": empty,
        "terminados": terminados,
    })

# view when the user wants to close the bid
@login_required(login_url='/login')
def terminar(request, product_id):
    winobj = Vencedor()

    ofobj = oferta.objects.get(listingid=product_id)
    winobj.vendedor = request.user.username
    winobj.email = request.user.email
    winobj.vencedor = ofobj.user
    winobj.listingid = product_id
    winobj.montante = ofobj.valor
    winobj.titulo = ofobj.title
    winobj.save()
    
    message = "Leilão Terminado. Pode entrar em contacto com o vencedor para o seu email " + winobj.vencedor
    msg_type = "success"

    if winobj:
        name =  winobj.vencedor
        email =  winobj.email
        messagem = 'A sua oferta foi licitada com sucesso. Por favor responda a este email com os seus contactos para entrar em contacto consigo e tratarmos do pagamento e entrega. Obrigado'

    send_mail(

        "Parabéns. O seu leilão encontrou um vencedor: " + name,
        email +" escreveu: " + messagem,
        email,
        ['mh.josevicente@gmail.com', 'josevcandido@gmail.com'],
        fail_silently=False
    )

        

    return render(request, "auctions/artigo.html", {
        "message": message,
        "msg_type": msg_type
    })

def search(request): 
    template = 'auctions/resultados.html'

    query = request.GET.get('q')

    if query:
        results = Increase.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:  
        results = Increase.objects.all()

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

def searchDecrease(request): 
    template = 'auctions/dresultados.html'

    query = request.GET.get('q')

    if query:
        results = Decrease.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:  
        results = Decrease.objects.all()

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


    return render(request, template, {'results': results})

def searchFixed(request): 
    template = 'auctions/fresultados.html'

    query = request.GET.get('q')

    if query:
        results = Fixed.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:  
        results = Fixed.objects.all()

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


    return render(request, template, {'results': results})

def SearchAll(request): 
    template = 'auctions/aresultados.html'

    query = request.GET.get('q')

    fresults = Fixed.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    dresults = Decrease.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    iresults = Increase.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {
        "fresults": fresults,
        "dresults": dresults,
        "iresults": iresults

    }
    

    """paginator = Paginator(fresults, 30)
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
    page_range = paginator.page_range[start_index:end_index]"""


    return render(request, template, context)


def contact(request): 
    template = 'auctions/contact.html'
 

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        messagem = request.POST['message']

        send_mail(

            "Contacto de: " + name,
            email +" escreveu: " + messagem,
            email,
            ['geral@misterhome.pt', 'josevcandido@gmail.com'],
            fail_silently=False
        )
        
        return render(request, template, {'name': name})
    else:  
        return render(request, template)

# view to create an Increased Listing
@login_required(login_url='/login')
def anunciar(request):
    

    form = Anunciar(request.POST, request.FILES)
    if form.is_valid():
        newpost = form.save()
        newpost.slug = slugify(newpost.title)
        newpost.save()
        #IMPORTANT
        try:
            form.save_m2m()
        except AttributeError:
            print("reload page")

    context = {
        'message': "O seu Leilão foi publicado por 7 dias. Obrigado",
        "msg_type": "success", 
        'form': form
    }

    return render(request, 'auctions/anunciar.html', context)


# view to create a Decrease Listing
@login_required(login_url='/login')
def criar(request):
    

    form = Criar(request.POST, request.FILES)
    if form.is_valid():
        newpost = form.save()
        newpost.slug = slugify(newpost.title)
        newpost.save()
        #IMPORTANT
        try:
            form.save_m2m()
        except AttributeError:
            print("reload page")

    context = {
        'message': "O seu Leilão foi publicado por 7 dias. Obrigado",
        "msg_type": "success", 
        'form': form
    }
    return render(request, 'auctions/criar.html', context)


# view to create a Fixed Listing
@login_required(login_url='/login')
def Vender(request):


    form = Venda(request.POST)
    if form.is_valid():
        newpost = form.save()
        newpost.slug = slugify(newpost.title)
        newpost.save()
        #IMPORTANT
        try:
            form.save_m2m()
        except AttributeError:
            print("reload page")

    context = {
        'message': "O seu Leilão foi publicado por 7 dias. Obrigado",
        "msg_type": "success", 
        'form': form
    }

    return render(request, 'auctions/shopnow.html', context)


def categ_smartphones(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request,"auctions/smartphones.html", context)

def categ_computadores(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request, 'auctions/computadores.html', context)

def categ_consolas(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request, 'auctions/consolas.html', context)

def categ_tablets(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }
    return render(request, 'auctions/tablets.html', context)

def categ_video(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')


    context = {
        'increases': increases,
        'decreases': decreases,
    }
    return render(request, 'auctions/videos.html', context)

def categ_televisores(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request, 'auctions/televisores.html', context)

def categ_drones(request):  

    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request, 'auctions/drones.html', context)

def categ_outros(request):  
    
    increases = Increase.objects.order_by('-created_at')
    decreases = Decrease.objects.order_by('-created_at')
    fixes = Fixed.objects.order_by('-created_at')

    total = increases.count() + decreases.count()

    context = {
        'increases': increases,
        'decreases': decreases,
        'total': total,
        'fixes': fixes
    }

    return render(request, 'auctions/outros.html', context)

def Privacy(request):
    return render(request, 'auctions/privacy.html')

def fixed(request):
    vendas = Fixed.objects.order_by("-created_at")
    common_tags = Fixed.tags.most_common()[:5]

    context = {
        'vendas': vendas,
        'common_tags': common_tags,
    }
    return render(request, 'auctions/fixed.html', context)

def vendas_detalhe(request, slug):

    common_tags = Fixed.tags.most_common()[:5]
    product = get_object_or_404(Fixed, slug=slug)
    return render(request, "auctions/details.html", {'product': product, "common_tags": common_tags})


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    vendas = Fixed.objects.filter(tags=tag)
    invertidos = Decrease.objects.filter(tags=tag)
    classicos = Increase.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'invertidos': invertidos,
        'classicos': classicos,
        'vendas': vendas
    }
    
    return render(request, 'auctions/tags.html', context)

