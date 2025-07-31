// Common models matching backend dto_common.py

export interface SeedDefaultsResponse {
  detail: string;
}

export interface UUIDResponse {
  id: string;
}

export interface CorporaSpec {
  countries?: string[] | null;
  institutions?: string[] | null;
  protocols?: string[] | null;
  parties?: string[] | null;
  speakers?: string[] | null;
  periods?: string[] | null;
}

export interface Corpora {
  id: string;
  label: string;
  texts: string[];
  countries?: string[] | null;
  institutions?: string[] | null;
  protocols?: string[] | null;
  parties?: string[] | null;
  speakers?: string[] | null;
  periods?: string[] | null;
}
