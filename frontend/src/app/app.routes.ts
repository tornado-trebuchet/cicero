import { Routes } from '@angular/router';
import { Frontpage } from './frontpage/frontpage';
import { Search } from './search/search';

export const routes: Routes = [
  { path: '', component: Frontpage },
  { path: 'search', component: Search },
];
