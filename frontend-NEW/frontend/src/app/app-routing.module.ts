import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DummyComponent } from './components/dummy/dummy.component';
import { Dummy2Component } from './components/dummy2/dummy2.component';
import { HomeComponent } from './components/home/home.component';

const routes: Routes = [
  { path: '', component: DummyComponent },
  { path: 'home', component: HomeComponent},
  { path: '2', component: Dummy2Component },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
