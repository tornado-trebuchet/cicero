// Enums matching backend v_enums.py

export enum CountryEnum {
  GERMANY = 'Germany',
  FRANCE = 'France'
}

export enum InstitutionTypeEnum {
  PARLIAMENT = 'Parliament',
  FEDERAL_ASSEMBLY = 'Feaderal Assembly'
}

export enum ProtocolTypeEnum {
  PLENARY = 'Plenary',
  HEARING = 'Hearing'
}

export enum GenderEnum {
  MALE = 'Male',
  FEMALE = 'Female',
  OTHER = 'Other'
}

export enum LanguageEnum {
  DE = 'german',
  FR = 'french',
  EN = 'english',
  M = 'missing'
}

export enum OwnerTypeEnum {
  COUNTRY = 'country',
  INSTITUTION = 'institution',
  PARTY = 'party',
  SPEAKER = 'speaker'
}
