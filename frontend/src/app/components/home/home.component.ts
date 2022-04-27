import { Component, OnInit } from '@angular/core';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  articles: any;

  constructor(private service: NewsService) { }

  ngOnInit(): void {
    this.getArticles();
  }

  getArticles() {
    this.service.getArticles().subscribe(
      res =>{
      console.log('articles...', res),
      this.articles = res}
    );
  }

  /* getDetails(value: any) {
    this.service.getArticleDetails(value).subscribe(
      data =>
      console.log('recebo valores?', data)
    )
  } */

}
