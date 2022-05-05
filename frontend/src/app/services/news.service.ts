import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  readonly APIUrl =  'https://backoffice-tejo.com/';
  // readonly APIUrl =  'http://127.0.0.1:8000/';

  // tornar coerente com os models.py
  categories = ['sociedade', 'cultura', 'saude', 'sustentabilidade', 'desporto',
  'politica', 'economia', 'empresas', 'lifestyle', 'tecnologia', 'startups'];

  categorias = [
    {name: 'sociedade', index:1},
    {name: 'economia', index:2},
    {name: 'cultura', index:3},
    {name: 'arte', index:4}
  ];

  constructor(private http:HttpClient) { }

  getArticles() {
    return this.http.get<any[]>(this.APIUrl + 'articles/');
  }

  getArticleDetails(value: any) {
    console.log('slug....', this.APIUrl + `articles/${value}`);
    return this.http.get<any[]>(this.APIUrl + `articles/${value}`);
  }

  getArticlesbyCat(cat: any) {
    return this.http.get<any[]>(this.APIUrl + `category/${cat}`);
  }

  getCats() {
    return this.categorias;
  }

}
