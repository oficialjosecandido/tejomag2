import { Component, OnInit } from '@angular/core';
import { NewsService } from 'src/app/services/news.service';

@Component({
  selector: 'app-cats-list',
  templateUrl: './cats-list.component.html',
  styleUrls: ['./cats-list.component.css']
})
export class CatsListComponent implements OnInit {

  categories: any;

  constructor(private service: NewsService) { }

  ngOnInit(): void {
    this.getCats();
  }

  getCats() {
    this.categories = this.service.getCats();
    console.log('categorias', this.categories)
  }

}
