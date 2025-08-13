import { Routes } from '@angular/router';
import { Frontpage } from './frontpage/frontpage';
import { Search } from './search/search';
import { Dashboard } from './dashboard/dashboard';

export const routes: Routes = [
  { path: '', component: Frontpage },
  { path: 'search', component: Search },
  { path: 'dashboard', component: Dashboard }
];
