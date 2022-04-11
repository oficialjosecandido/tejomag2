from django.urls import path, re_path
from django.contrib.auth import views as auth_views 

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("llogin", views.login_view, name="llogin"),
    path("llogout", views.logout_view, name="llogout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("mocks", views.mocks, name="mocks"),
    path('createNews', views.createNews, name="createNews"),

    #verificar se este URL está a funcionar
    path('news/<slug:slug>', views.newsDetails, name="newsDetails"),
    path('BO/news/<slug:slug>', views.BOnewsDetails, name="BOnewsDetails"),



    #para servir o frontEnd
    re_path(r'^news/$', views.newsAPI),
    # re_path(r'^banners/$', views.bannersApi),
    # re_path(r'^banners5/$', views.banners5Api),
    # re_path(r'^fnewsLatest/$', views.latestFlashNewsAPI),


    path("activelisting", views.activelisting, name="activelisting"),
    path("winners", views.winners, name="winners"),
    path("viewlisting/<int:product_id>", views.viewlisting, name="viewlisting"),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path("addtowatchlist/<int:product_id>",
         views.addtowatchlist, name="addtowatchlist"),
    path("addcomment/<int:product_id>", views.addcomment, name="addcomment"),
    path("category/<str:categ>", views.category, name="category"),
    path("closebid/<int:product_id>", views.closebid, name="closebid"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("resultados", views.search, name="resultados"),
    path('anunciar', views.anunciar, name="anunciar"),
    path('contact', views.contact, name="contact"),
    path('closedbid/<int:product_id>"', views.closebid, name="closedbid"),
    path('vencidos', views.vencidos, name="vencidos"),
    path('publicados', views.publicados, name='publicados'),
    path('watchlist', views.dwatchlist, name='watchlist'),
    path('dhistorico', views.dhistorico, name='dhistorico'),
    path('tc', views.tc, name='tc'),  
    path('pp', views.pp, name='pp'),        

    path("smartphones", views.categ_smartphones, name="smartphones"),
    path("televisores", views.categ_televisores, name="televisores"),
    path("consolas", views.categ_consolas, name="consolas"),
    path("computadores", views.categ_computadores, name="computadores"),
    path("gadgets", views.categ_gadgets, name="gadgets"),
    path("drones", views.categ_drones, name="drones"),
    path("video", views.categ_video, name="video"),
    path("outros", views.categ_outros, name="outros"),
    

]
