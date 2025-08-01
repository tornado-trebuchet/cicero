import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { BaseApiService } from '../base-api.service';
import { 
  SeedDefaultsResponse, 
  UUIDResponse, 
  CorporaSpec, 
  Corpora 
} from '../../models';

@Injectable({
  providedIn: 'root'
})
export class CommonService extends BaseApiService {
  


  // Mock health check endpoint (replace with actual when backend adds it)
  getHealthCheck(): Observable<any> {
    return this.get('/')  // FastAPI root endpoint
      .pipe(
        catchError(() => {
          // Return mock health data if root fails
          return of({ status: 'healthy', timestamp: new Date().toISOString() });
        })
      );
  }

  getVersion(): Observable<any> {
    return this.get('/version')
      .pipe(
        catchError(() => {
          return of({ version: '1.0.0', api: 'cicero-backend' });
        })
      );
  }


  getCorporaById(id: string): Observable<Corpora> {
    return this.get<Corpora>(`/common/corpora/${id}`);
  }
}
