import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BaseApiService } from '../base-api.service';
import { SeedDefaultsResponse, UUIDResponse, CorporaSpec } from '../../models';

@Injectable({
  providedIn: 'root'
})
export class AdminService extends BaseApiService {
  constructor(protected override http: HttpClient) {
    super(http);
  }

  // Development endpoints
  seedDefaults(): Observable<SeedDefaultsResponse> {
    return this.post<SeedDefaultsResponse>('/develop/seed', {});
  }

  seedFetchExtract(): Observable<any> {
    return this.post('/develop/seed_fetch_extract', {});
  }

  // Corpora management
  assembleCorpora(spec: CorporaSpec): Observable<UUIDResponse> {
    return this.post<UUIDResponse>('/common/corpora/assemble', spec);
  }
}