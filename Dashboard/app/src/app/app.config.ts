import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter, withComponentInputBinding, withHashLocation } from '@angular/router';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    // Hash URLs so the built app works from any static folder; route params bind to inputs (dp, key).
    provideRouter(routes, withHashLocation(), withComponentInputBinding())
  ]
};
