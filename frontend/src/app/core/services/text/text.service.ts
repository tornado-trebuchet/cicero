import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseApiService } from '../base-api.service';
import { 
  Protocol, 
  Speech, 
  SpeechText, 
  RawText, 
  CleanText 
} from '../../models';

@Injectable({
  providedIn: 'root'
})
export class TextService extends BaseApiService {
  
  // Protocols
  getProtocols(): Observable<Protocol[]> {
    return this.get<Protocol[]>('/protocols');
  }

  getProtocolById(id: string): Observable<Protocol> {
    return this.get<Protocol>(`/protocols/${id}`);
  }

  getProtocolsByCountryId(countryId: string): Observable<Protocol[]> {
    return this.get<Protocol[]>(`/protocols/by_country/${countryId}`);
  }

  getProtocolsByInstitutionId(institutionId: string): Observable<Protocol[]> {
    return this.get<Protocol[]>(`/protocols/by_institution/${institutionId}`);
  }

  getProtocolsByInstitutionAndPeriod(institutionId: string, periodId: string): Observable<Protocol[]> {
    return this.get<Protocol[]>(`/protocols/by_institution_and_period/${institutionId}/${periodId}`);
  }

  getProtocolsByDateRange(startDate: string, endDate: string): Observable<Protocol[]> {
    return this.get<Protocol[]>(`/protocols/by_date_range/${startDate}/${endDate}`);
  }

  // Speeches
  getSpeechById(id: string): Observable<Speech> {
    return this.get<Speech>(`/speeches/${id}`);
  }

  getSpeechesByProtocolId(protocolId: string): Observable<Speech[]> {
    return this.get<Speech[]>(`/speeches/by_protocol/${protocolId}`);
  }

  getSpeechesBySpeakerId(speakerId: string): Observable<Speech[]> {
    return this.get<Speech[]>(`/speeches/by_speaker/${speakerId}`);
  }

  getSpeechesByDateRange(startDate: string, endDate: string): Observable<Speech[]> {
    return this.get<Speech[]>(`/speeches/by_date_range/${startDate}/${endDate}`);
  }

  // Speech Text
  getSpeechTextById(speechTextId: string): Observable<SpeechText> {
    return this.get<SpeechText>(`/speech_texts/${speechTextId}`);
  }
}
