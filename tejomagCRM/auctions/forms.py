from django import forms

from .models import *


class Anunciar(forms.ModelForm):  
    class Meta:  
        model = Listing
        template_name = 'anunciar.html'
        fields = ['seller', 'title', 'description', 'excerpt', 'starting_bid', 'tags', 'imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6']

        widgets = {
            'seller': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Vendedor'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'starting_bid': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Valor Mínimo (€)'}),            

        }

class newsForm(forms.ModelForm):  
    class Meta:  
        model = News
        template_name = 'createNews.html'
        fields = ['author', 'title', 'p1', 'excerpt', 'category', 'tags', 'status', 'image1_link', 'image2_link', 'image3_link']

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Autor'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'p1': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
            # 'starting_bid': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Valor Mínimo (€)'}),            

        }

class articleForm(forms.ModelForm):  
    class Meta:  
        model = Article
        template_name = 'createNews.html'
        fields = ['author', 'title', 'p1', 'excerpt', 'category', 'type', 'image1_link', 'image2_link', 'image3_link']

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Autor'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'p1': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
        }