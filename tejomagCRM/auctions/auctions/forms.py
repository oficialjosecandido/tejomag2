from django import forms

from .models import *



class Venda(forms.ModelForm):
    class Meta:
        model = Fixed
        template_name = 'shopnow.html'
        fields = ['seller','title', 'description', 'excerpt', 'price', 'category', 'tags',
        'shipping_cost', 'imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6']  

        widgets = {
            'seller': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username (igual ao username)'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'price': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Preço (€)'}),
            'shipping_cost': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Custo do Envio (€)'}),
            'tags': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Tags'}),
            

        } 


class Anunciar(forms.ModelForm):  
    class Meta:  
        model = Increase
        template_name = 'anunciar.html'
        fields = ['seller','title', 'description', 'excerpt', 'starting_bid', 'category', 'tags', 'shipping_cost', 'imagem1', 'imagem2', 'imagem3',]

        widgets = {
            'seller': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username (igual ao username)'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'starting_bid': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Valor Mínimo (€)'}),
            'shipping_cost': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Custo do Envio (€)'}),
            

        }


class Criar(forms.ModelForm):  
    class Meta:  
        model = Decrease
        template_name = 'criar.html'
        fields = [ 'seller', 'title', 'description', 'excerpt', 'pbase', 'pmin', 'category', 'tags', 'imagem1', 'imagem2', 'imagem3', ]


        widgets = {
            'seller': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username (igual ao username)'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Descrição'}),
            'excerpt': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'pbase': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Valor Base (€)'}),
            'pmin': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Valor Mínimo (€)'})            

        }