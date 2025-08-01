import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseApiService } from '../base-api.service';
import { 
  Country, 
  Institution, 
  Party, 
  Period, 
  Speaker 
} from '../../models';

@Injectable({
  providedIn: 'root'
})
export class ContextService extends BaseApiService {
  
  // Countries
  getCountries(): Observable<Country[]> {
    return this.get<Country[]>('/countries');
  }

  getCountryById(id: string): Observable<Country> {
    return this.get<Country>(`/countries/${id}`);
  }

  getCountryByEnum(countryEnum: string): Observable<Country> {
    return this.get<Country>(`/countries/by_enum/${countryEnum}`);
  }

  // Institutions
  getInstitutions(): Observable<Institution[]> {
    return this.get<Institution[]>('/institutions');
  }

  getInstitutionById(id: string): Observable<Institution> {
    return this.get<Institution>(`/institutions/${id}`);
  }

  getInstitutionsByType(type: string): Observable<Institution[]> {
    return this.get<Institution[]>(`/institutions/by_type/${type}`);
  }

  // Parties
  getParties(): Observable<Party[]> {
    return this.get<Party[]>('/parties');
  }

  getPartyById(id: string): Observable<Party> {
    return this.get<Party>(`/parties/${id}`);
  }

  getPartyByName(name: string): Observable<Party> {
    return this.get<Party>(`/parties/by_name/${name}`);
  }

  // Periods
  getPeriods(): Observable<Period[]> {
    return this.get<Period[]>('/periods');
  }

  getPeriodById(id: string): Observable<Period> {
    return this.get<Period>(`/periods/${id}`);
  }

  getPeriodsByOwnerId(ownerId: string): Observable<Period[]> {
    return this.get<Period[]>(`/periods/by_owner_id/${ownerId}`);
  }

  getPeriodsByOwner(ownerId: string, ownerType: string): Observable<Period[]> {
    return this.get<Period[]>(`/periods/by_owner/${ownerId}/${ownerType}`);
  }

  getPeriodByLabel(label: string): Observable<Period> {
    return this.get<Period>(`/periods/by_label/${label}`);
  }

  // Speakers
  getSpeakerById(id: string): Observable<Speaker> {
    return this.get<Speaker>(`/speakers/${id}`);
  }

  getSpeakersByName(name: string): Observable<Speaker[]> {
    return this.get<Speaker[]>(`/speakers/by_name/${name}`);
  }
}
