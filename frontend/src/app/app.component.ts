import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  readonly APIUrl =  'http://127.0.0.1:8000/';
  news: any;

  constructor(private http:HttpClient) {}

  ngOnInit() {
    console.log('estou vivo');
    this.getNews();
  }

  getBanners():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'news/');
  }

  getNews() {
    this.getBanners().subscribe(
      res =>
      // console.log('news', res)
      this.news = res
    );
  }

  getDetails(value: any) {
    console.log('slug....', this.APIUrl + `news/${value}`);
    return this.http.get<any[]>(this.APIUrl + `news/${value}`);
  }
}
