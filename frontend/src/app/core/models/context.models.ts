// Context models matching backend dto_context.py
import { CountryEnum, InstitutionTypeEnum, OwnerTypeEnum } from './enums';

export interface Country {
  id: string;
  country: CountryEnum;
  institutions?: string[] | null;
  periodisation?: string[] | null;
  parties?: string[] | null;
  speakers?: string[] | null;
}

export interface Institution {
  id: string;
  country_id: string;
  type: InstitutionTypeEnum;
  label: string;
  protocols?: string[] | null;
  periodisation?: string[] | null;
  metadata?: Record<string, any> | null;
}

export interface Party {
  id: string;
  country_id: string;
  party_name: string;
  party_program?: string | null;
  speakers?: string[] | null;
}

export interface Period {
  id: string;
  owner_id: string;
  owner_type: OwnerTypeEnum;
  label: string;
  start_date?: string | null; // ISO date string
  end_date?: string | null;   // ISO date string
}

export interface Speaker {
  id: string;
  country_id: string;
  name: string;
  speeches?: string[] | null;
  party?: string | null;
  role?: string | null;
  birth_date?: string | null; // ISO date string
  gender?: string | null;
}
