import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  readonly APIUrl =  'http://backoffice-tejo.com/';
  // readonly APIUrl =  'http://127.0.0.1:8000/';

  constructor(private http:HttpClient) { }

  getArticles() {
    return this.http.get<any[]>(this.APIUrl + 'articles/');
  }

  getArticleDetails(value: any) {
    console.log('slug....', this.APIUrl + `articles/${value}`);
    return this.http.get<any[]>(this.APIUrl + `articles/${value}`);
  }

}
