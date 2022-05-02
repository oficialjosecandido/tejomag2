import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { HttpClientModule } from '@angular/common/http';
import { HomeComponent } from './components/home/home.component';
import { ArticlesDetailsComponent } from './components/articles/articles-details/articles-details.component';
import { DummyComponent } from './components/dummy/dummy.component';
import { TermsComponent } from './components/landings/terms/terms.component';
import { EstatutoEditorialComponent } from './components/landings/estatuto-editorial/estatuto-editorial.component';
import { FichaTecnicaComponent } from './components/landings/ficha-tecnica/ficha-tecnica.component';
import { PrivacyComponent } from './components/landings/privacy/privacy.component';
import { CookiesComponent } from './components/landings/cookies/cookies.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ArticlesDetailsComponent,
    DummyComponent,
    TermsComponent,
    EstatutoEditorialComponent,
    FichaTecnicaComponent,
    PrivacyComponent,
    CookiesComponent,

  ],
  imports: [
    BrowserModule.withServerTransition({ appId: 'serverApp' }),
    HttpClientModule,
    AppRoutingModule,
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: environment.production,
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
