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
    path('createArticle', views.createArticle, name="createArticle"),

    path('contact', views.ContactView.as_view(), name='contact'),

    #verificar se este URL está a funcionar
    path('news/<slug:slug>', views.newsDetails, name="newsDetails"),
    path('BO/news/<slug:slug>', views.BOnewsDetails, name="BOnewsDetails"),
    path('articles/<slug:slug>', views.articleDetails, name="newsDetails"),
    path('BO/articles/<slug:slug>', views.BOnewsDetails, name="BOnewsDetails"),



    #para servir o frontEnd
    re_path(r'^news/$', views.newsAPI),
    re_path(r'^articles', views.articlesSprintAPI),
    # re_path(r'^banners/$', views.bannersApi),
    # re_path(r'^banners5/$', views.banners5Api),
    # re_path(r'^fnewsLatest/$', views.latestFlashNewsAPI),


    
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
    path("resultados", views.search, name="resultados"),
    path('contact', views.contact, name="contact"),
]
