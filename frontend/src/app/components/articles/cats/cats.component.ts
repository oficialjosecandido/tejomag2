import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-cats',
  templateUrl: './cats.component.html',
  styleUrls: ['./cats.component.css']
})
export class CatsComponent implements OnInit {

  articles: any;
  category!: string | null;

  constructor(private service: NewsService, private route:ActivatedRoute) { }

  ngOnInit(): void {
    const cat = this.route.snapshot.paramMap.get('category');
    this.category = cat
    this.getArticles(cat);
  }

  getArticles(value: any) {
    this.service.getArticlesbyCat(value).subscribe(
      res =>{
      console.log('articles by category...', value,res),
      this.articles = res}
    );
  }

}
