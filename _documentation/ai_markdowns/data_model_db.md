# Database Data Model Documentation

This document provides a comprehensive overview of the PostgreSQL database schema implemented through SQLAlchemy ORM models for the Cicero project. The database is designed to store parliamentary speech data, context information, and text processing results.

## Overview

The database consists of three main domains:
- **Context**: Countries, institutions, parties, speakers, and periods
- **Text**: Protocols, speeches, and various text processing stages
- **Common**: Corpora for grouping speeches

## Database Schema

### Context Domain

#### Countries Table (`countries`)
Stores information about countries in the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `country` | ENUM(CountryEnum) | NOT NULL, UNIQUE | Country name (Germany, France) |

**Relationships:**
- One-to-many with `institutions`
- One-to-many with `speakers`
- One-to-many with `parties`
- One-to-many with `periods` (via polymorphic relationship)

#### Institutions Table (`institutions`)
Represents parliamentary institutions within countries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `country_id` | UUID | FOREIGN KEY → countries.id, NOT NULL | Reference to country |
| `institution_type` | ENUM(InstitutionTypeEnum) | NOT NULL | Type (Parliament, Federal Assembly) |
| `label` | VARCHAR | NOT NULL | Institution name/label |
| `meta_data` | JSONB | NOT NULL | Additional metadata |

**Relationships:**
- Many-to-one with `countries`
- One-to-many with `protocols`

#### Parties Table (`parties`)
Political parties within countries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `country_id` | UUID | FOREIGN KEY → countries.id, NOT NULL | Reference to country |
| `label` | VARCHAR | NOT NULL | Party label/code |
| `party_name` | VARCHAR | NOT NULL | Full party name |
| `party_program` | TEXT | NULLABLE | Party program description |

**Relationships:**
- Many-to-one with `countries`
- One-to-many with `speakers` (members)

#### Speakers Table (`speakers`)
Individual speakers/politicians.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `country_id` | UUID | FOREIGN KEY → countries.id, NOT NULL | Reference to country |
| `party_id` | UUID | FOREIGN KEY → parties.id, NULLABLE | Reference to party |
| `name` | VARCHAR | NOT NULL | Speaker's name |
| `role` | VARCHAR | NULLABLE | Speaker's role/position |
| `birth_date` | DATE | NULLABLE | Date of birth |
| `gender` | ENUM(GenderEnum) | NULLABLE | Gender (Male, Female, Other) |

**Indexes:**
- `idx_speaker_party_id` on `party_id`
- `idx_speaker_name` on `name`

**Relationships:**
- Many-to-one with `countries`
- Many-to-one with `parties`
- One-to-many with `speeches`

#### Periods Table (`periods`)
Time periods for various entities (polymorphic relationship).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `owner_id` | UUID | NOT NULL | ID of the owning entity |
| `owner_type` | ENUM(OwnerTypeEnum) | NOT NULL | Type of owner (country, institution, party, speaker) |
| `label` | VARCHAR | NOT NULL | Period label |
| `start_date` | TIMESTAMP | NOT NULL | Period start date |
| `end_date` | TIMESTAMP | NOT NULL | Period end date |
| `description` | VARCHAR | NULLABLE | Period description |

**Indexes:**
- `idx_period_owner` on (`owner_id`, `owner_type`)
- `idx_period_dates` on (`start_date`, `end_date`)

### Text Domain

#### Protocols Table (`protocols`)
Parliamentary session protocols/documents.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `institution_id` | UUID | FOREIGN KEY → institutions.id, NOT NULL | Reference to institution |
| `label` | VARCHAR | NULLABLE | Protocol label |
| `agenda` | JSONB | NULLABLE | Session agenda |
| `file_source` | VARCHAR | NOT NULL | Source file path/reference |
| `protocol_type` | ENUM(ProtocolTypeEnum) | NOT NULL | Type (Plenary, Hearing) |
| `date` | TIMESTAMP WITH TIME ZONE | NOT NULL | Protocol date |
| `protocol_text` | VARCHAR | NOT NULL | Full protocol text |
| `metadata_data` | JSONB | NOT NULL | Additional metadata |

**Indexes:**
- `idx_protocol_institution` on `institution_id`
- `idx_protocol_date` on `date`
- `idx_protocol_institution_date` on (`institution_id`, `date`)

**Relationships:**
- Many-to-one with `institutions`
- One-to-many with `speeches`

#### Speeches Table (`speeches`)
Individual speeches within protocols.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `protocol_id` | UUID | FOREIGN KEY → protocols.id, NOT NULL | Reference to protocol |
| `speaker_id` | UUID | FOREIGN KEY → speakers.id, NOT NULL | Reference to speaker |
| `protocol_order` | INTEGER | NOT NULL | Order within protocol |
| `meta_data` | JSONB | NULLABLE | Speech metadata |

**Indexes:**
- `idx_speech_protocol` on `protocol_id`
- `idx_speech_speaker` on `speaker_id`

**Relationships:**
- Many-to-one with `protocols`
- Many-to-one with `speakers`
- One-to-one with `speech_texts`
- One-to-one with `speech_metrics` (optional)
- Many-to-many with `corpora`

#### Speech Texts Table (`speech_texts`)
Central hub for all text processing of speeches.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_id` | UUID | FOREIGN KEY → speeches.id, NOT NULL, UNIQUE | Reference to speech |
| `language_code` | ENUM(LanguageEnum) | NULLABLE | Language (german, french, english, missing) |
| `metrics` | JSONB | NULLABLE | Text processing metrics |

**Indexes:**
- `idx_text_speech` on `speech_id`

**Relationships:**
- One-to-one with `speeches`
- One-to-one with `raw_texts`
- One-to-one with `clean_texts` (optional)
- One-to-one with `split_texts` (optional)
- One-to-one with `tokenized_texts` (optional)
- One-to-one with `text_ngrams` (optional)
- One-to-one with `translated_texts` (optional)

#### Text Processing Tables

##### Raw Texts Table (`raw_texts`)
Original, unprocessed speech text.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id, NOT NULL, UNIQUE | Reference to speech text |
| `text` | TEXT | NOT NULL | Raw speech text |

##### Clean Texts Table (`clean_texts`)
Cleaned and preprocessed speech text.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id ON DELETE CASCADE, NOT NULL, UNIQUE | Reference to speech text |
| `clean_text` | TEXT | NOT NULL | Cleaned speech text |

##### Split Texts Table (`split_texts`)
Text split into sentences.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id, NOT NULL, UNIQUE | Reference to speech text |
| `sentences` | VARCHAR ARRAY | NOT NULL | Array of sentences |

##### Tokenized Texts Table (`tokenized_texts`)
Tokenized text for analysis.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id, NOT NULL, UNIQUE | Reference to speech text |
| `tokens` | VARCHAR ARRAY | NOT NULL | Array of tokens |

##### Text N-grams Table (`text_ngrams`)
N-gram tokens for text analysis.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id, NOT NULL, UNIQUE | Reference to speech text |
| `ngram_tokens` | VARCHAR ARRAY | NOT NULL | Array of n-gram tokens |

##### Translated Texts Table (`translated_texts`)
Translated versions of speeches.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_text_id` | UUID | FOREIGN KEY → speech_texts.id, NOT NULL, UNIQUE | Reference to speech text |
| `translated_text` | TEXT | NOT NULL | Translated speech text |

#### Speech Metrics Table (`speech_metrics`)
Analysis metrics and results for speeches.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `speech_id` | UUID | FOREIGN KEY → speeches.id ON DELETE CASCADE, NOT NULL, UNIQUE | Reference to speech |
| `dominant_topics` | JSONB | NULLABLE | Topic modeling results |
| `sentiment` | JSONB | NULLABLE | Sentiment analysis results |
| `dynamic_codes` | JSONB | NULLABLE | Dynamic coding results |

### Common Domain

#### Corpora Table (`corpora`)
Collections/groupings of speeches for analysis.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier |
| `label` | VARCHAR | NOT NULL | Corpus label/name |
| `countries` | UUID ARRAY | NULLABLE | Array of country IDs |
| `institutions` | UUID ARRAY | NULLABLE | Array of institution IDs |
| `periods` | UUID ARRAY | NULLABLE | Array of period IDs |
| `parties` | UUID ARRAY | NULLABLE | Array of party IDs |
| `speakers` | UUID ARRAY | NULLABLE | Array of speaker IDs |

**Relationships:**
- Many-to-many with `speeches` via `corpora_speeches` junction table

#### Corpora-Speeches Junction Table (`corpora_speeches`)
Many-to-many relationship between corpora and speeches.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `corpora_id` | UUID | FOREIGN KEY → corpora.id, PRIMARY KEY | Reference to corpus |
| `speech_id` | UUID | FOREIGN KEY → speeches.id, PRIMARY KEY | Reference to speech |

## Enums

### CountryEnum
- `GERMANY`: "Germany"
- `FRANCE`: "France"

### InstitutionTypeEnum
- `PARLIAMENT`: "Parliament"
- `FEDERAL_ASSEMBLY`: "Federal Assembly"

### ProtocolTypeEnum
- `PLENARY`: "Plenary"
- `HEARING`: "Hearing"

### GenderEnum
- `MALE`: "Male"
- `FEMALE`: "Female"
- `OTHER`: "Other"

### LanguageEnum
- `DE`: "german"
- `FR`: "french"
- `EN`: "english"
- `M`: "missing"

### OwnerTypeEnum
- `COUNTRY`: "country"
- `INSTITUTION`: "institution"
- `PARTY`: "party"
- `SPEAKER`: "speaker"

## Relationship Patterns

### Cascade Behaviors
- **CASCADE DELETE**: Text processing tables cascade delete when their parent speech_text is deleted
- **PASSIVE DELETES**: Most foreign key relationships use passive deletes for performance
- **DELETE ORPHAN**: One-to-many relationships typically use delete-orphan to clean up orphaned records

### Indexing Strategy
The database uses strategic indexing for:
- Foreign key relationships
- Date-based queries
- Name searches
- Polymorphic owner relationships

### JSONB Usage
JSONB columns are used for:
- Flexible metadata storage
- Analysis results (topics, sentiment)
- Configuration data (agenda, metrics)

This design provides a flexible, scalable foundation for storing and analyzing parliamentary speech data with comprehensive text processing capabilities.
