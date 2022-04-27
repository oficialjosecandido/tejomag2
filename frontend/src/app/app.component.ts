import { Component } from '@angular/core';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'TEJOmag';


  constructor() {}

  ngOnInit() {
  }

  /* getBanners():Observable<any[]>{
    return this.http.get<any[]>(this.APIUrl + 'news/');
  }



  getDetails(value: any) {
    console.log('slug....', this.APIUrl + `news/${value}`);
    return this.http.get<any[]>(this.APIUrl + `news/${value}`);
  } */
}
