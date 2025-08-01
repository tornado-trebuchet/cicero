// Text models matching backend dto_text.py
import { LanguageEnum, ProtocolTypeEnum } from './enums';

export interface Protocol {
  id: string;
  institution_id: string;
  date: string; // ISO date string
  protocol_type: ProtocolTypeEnum;
  protocol_text: string;
  agenda?: Record<string, string[]> | null;
  file_source?: string | null;
  protocol_speeches?: string[] | null;
  metadata?: Record<string, any> | null;
}

export interface SpeechText {
  id: string;
  speech_id: string;
  raw_text: string;
  language_code: LanguageEnum;
  clean_text?: string | null;
  translated_text?: string | null;
  sentences?: string | null;
  tokens?: string | null;
  ngram_tokens?: string | null;
  text_metrics?: Record<string, number | null> | null;
}

export interface Speech {
  id: string;
  protocol_id: string;
  speaker_id: string;
  text: string;
  metrics?: Record<string, any> | null;
  metadata?: Record<string, any> | null;
}

export interface RawText {
  id: string;
  speech_text_id: string;
  raw_text: string;
}

export interface CleanText {
  id: string;
  speech_text_id: string;
  clean_text: string;
}
