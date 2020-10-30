import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';


if (environment.production) {
  enableProdMode();

  if(window){
    window.console.log = window.console.warn = window.console.info = function(){
      // Don't log anything. to prevent logging in production
    };
  }

}

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.error(err));
