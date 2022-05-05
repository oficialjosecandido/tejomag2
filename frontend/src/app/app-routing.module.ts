import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { ArticlesDetailsComponent } from './components/articles/articles-details/articles-details.component';
import { CatsComponent } from './components/articles/cats/cats.component';
import { DummyComponent } from './components/dummy/dummy.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  {path: 'home', component: HomeComponent},
  {path: 'dummy', component: DummyComponent},
  { path: 'article/:slug', component:ArticlesDetailsComponent},
  { path: 'category/:category', component:CatsComponent},
  { path: '', redirectTo: '/dummy', pathMatch: 'full' },
  { path: '**', component: AppComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
