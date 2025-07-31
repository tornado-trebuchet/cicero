import { Routes } from '@angular/router';
import { ApiTestComponent } from './features/api-test.component';

export const routes: Routes = [
  { path: '', redirectTo: '/api-test', pathMatch: 'full' },
  { path: 'api-test', component: ApiTestComponent },
  { path: '**', redirectTo: '/api-test' }
];
