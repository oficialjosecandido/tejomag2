import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-articles-details',
  templateUrl: './articles-details.component.html',
  styleUrls: ['./articles-details.component.css']
})
export class ArticlesDetailsComponent implements OnInit {

  article: any;

  constructor(private route: ActivatedRoute, private service: NewsService ) { }

  ngOnInit(): void {
    this.loadArticle();
  }

  loadArticle(){
    const articleId = this.route.snapshot.paramMap.get('slug');
    console.log('id do artigo....', articleId);
    this.service.getArticleDetails(articleId).subscribe(
      data => {
        console.log('recebo valores?', data),
        this.article = data
      }

    )
    /* this.service.getEmployee(EmployeeId).subscribe(
      (data) => {
        this.Employee = data[0];
        console.log('this profile info', data[0]);
        this.ImageUrl = this.mediaLocation + this.Employee.PhotoFileName;
      },
      error => {
        this.error = error;
      }
    );  */
  }

}
