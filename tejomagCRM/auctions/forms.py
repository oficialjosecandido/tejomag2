from django import forms
from .models import *

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
        }

class articleForm(forms.ModelForm):  
    class Meta:  
        model = Article
        template_name = 'createNews.html'
        fields = ['author', 'title',  'excerpt', 'category', 'type','p1', 'p2', 'p3',  'image1_link', 'image2_link', 'image3_link']

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Autor'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Título'}),
            'excerpt': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Excerto (máximo 100 palavras)'}),
            'p1': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Parágrafo1'}),
            'p2': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Parágrafo2'}),
            'p3': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Parágrafo3'}),
            'p4': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Parágrafo4'}),
        }