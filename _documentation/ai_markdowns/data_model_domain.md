# Domain Data Model Documentation

This document describes the domain model structure of the Cicero system, which handles parliamentary speech analysis and political discourse processing.

## Domain Model Architecture

The system follows Domain-Driven Design (DDD) principles with a clear separation between:
- **Entities**: Objects with unique identity that can change over time
- **Value Objects**: Immutable objects defined by their attributes
- **Aggregate Roots**: Entities that serve as entry points to aggregates
- **Base Classes**: Common foundation classes

## Base Classes

### Entity
**File**: `src/domain/models/base_entity.py`
- Base class for all entities with unique identity
- Properties: `id` (UUID, immutable)
- Implements equality based on ID and hash functionality

### ValueObject
**File**: `src/domain/models/base_vo.py`
- Base class for immutable value objects
- Implements equality based on all attributes
- Provides consistent hashing and representation

### AggregateRoot
**File**: `src/domain/models/base_aggregate.py`
- Extends Entity for aggregate boundaries
- Properties: `id`, `version` (for optimistic locking)
- Methods: `increment_version()`

## Common Value Objects

### UUID
**File**: `src/domain/models/common/v_common.py`
- Wrapper for Python UUID with validation
- Methods: `new()` (static factory), `value` property
- Ensures type safety and consistency across the domain

### DateTime
**File**: `src/domain/models/common/v_common.py`
- Immutable datetime wrapper with timezone support
- Methods: `now()`, `from_timestamp()`, `to_timestamp()`, `to_iso()`, `to_date()`
- Handles date/datetime conversion automatically

### HttpUrl
**File**: `src/domain/models/common/v_common.py`
- URL validation and encapsulation
- Validates scheme and netloc presence
- Immutable once created

### MetadataPlugin
**File**: `src/domain/models/common/v_metadata_plugin.py`
- Dynamic metadata storage for extensibility
- Properties: `data` (dictionary)
- Methods: `set_property()`, `get_property()`, `get_properties()`, `remove_property()`

## Enumerations

### CountryEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `GERMANY`, `FRANCE`
- Represents supported countries in the system

### InstitutionTypeEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `PARLIAMENT`, `FEDERAL_ASSEMBLY`
- Types of political institutions

### ProtocolTypeEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `PLENARY`, `HEARING`
- Types of parliamentary sessions

### GenderEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `MALE`, `FEMALE`, `OTHER`
- Speaker gender classification

### LanguageEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `DE` (german), `FR` (french), `EN` (english), `M` (missing)
- Language codes for text processing

### OwnerTypeEnum
**File**: `src/domain/models/common/v_enums.py`
- Values: `COUNTRY`, `INSTITUTION`, `PARTY`, `SPEAKER`
- Types of entities that can own periods

## Context Domain

### Country (Aggregate Root)
**File**: `src/domain/models/context/a_country.py`
- Properties:
  - `id`: UUID
  - `country`: CountryEnum
  - `periodisation`: Optional[List[UUID]] - historical periods
  - `institutions`: Optional[List[UUID]] - government institutions
  - `parties`: Optional[List[UUID]] - political parties
  - `speakers`: Optional[List[UUID]] - political speakers
- Methods: `add_speaker()`

### Institution (Entity)
**File**: `src/domain/models/context/e_institution.py`
- Properties:
  - `id`: UUID
  - `country_id`: UUID (foreign key to Country)
  - `type`: InstitutionTypeEnum
  - `label`: Label
  - `protocols`: List[UUID] - parliamentary sessions
  - `periodisation`: Optional[List[UUID]] - time periods
  - `metadata`: Optional[MetadataPlugin]

### Party (Entity)
**File**: `src/domain/models/context/e_party.py`
- Properties:
  - `id`: UUID
  - `country_id`: UUID (foreign key to Country)
  - `party_name`: PartyName
  - `party_program`: Optional[PartyProgramText]
  - `speakers`: Optional[List[UUID]] - party members

### Speaker (Entity)
**File**: `src/domain/models/context/e_speaker.py`
- Properties:
  - `id`: UUID
  - `country_id`: UUID (foreign key to Country)
  - `name`: Name
  - `speeches`: Optional[List[UUID]] - delivered speeches
  - `party`: Optional[UUID] (foreign key to Party)
  - `role`: Optional[str] - political role/position
  - `birth_date`: Optional[DateTime]
  - `gender`: Optional[GenderEnum]

### Period (Entity)
**File**: `src/domain/models/context/e_period.py`
- Properties:
  - `id`: UUID
  - `owner_id`: UUID - entity that owns this period
  - `owner_type`: OwnerTypeEnum
  - `label`: Label
  - `start_date`: DateTime
  - `end_date`: DateTime
  - `description`: Optional[str]
- Methods: `to_range_dict()`
- Validation: start_date must be before end_date

### Context Value Objects

#### Label
**File**: `src/domain/models/context/v_label.py`
- Properties: `value`: str
- Used for naming institutional entities

#### Name
**File**: `src/domain/models/context/v_name.py`
- Properties: `value`: str
- Represents speaker names

#### PartyName
**File**: `src/domain/models/context/v_party_name.py`
- Properties: `value`: str
- Represents political party names

## Text Domain

### Protocol (Aggregate Root)
**File**: `src/domain/models/text/a_protocol.py`
- Properties:
  - `id`: UUID
  - `institution_id`: UUID (foreign key to Institution)
  - `date`: DateTime - session date
  - `protocol_type`: ProtocolTypeEnum
  - `protocol_text`: ProtocolText - full session text
  - `file_source`: HttpUrl - original document source
  - `label`: Optional[Label]
  - `agenda`: Optional[Agenda] - session agenda
  - `protocol_speeches`: List[UUID] - contained speeches
  - `metadata`: Optional[MetadataPlugin]
- Methods: `add_speech()`

### Speech (Entity)
**File**: `src/domain/models/text/a_speech.py`
- Properties:
  - `id`: UUID
  - `protocol_id`: UUID (foreign key to Protocol)
  - `speaker_id`: UUID (foreign key to Speaker)
  - `text`: UUID (foreign key to SpeechText)
  - `protocol_order`: int - order within protocol
  - `metadata`: Optional[MetadataPlugin]
  - `metrics`: Optional[MetricsPlugin] - analytical metrics

### SpeechText (Aggregate Root)
**File**: `src/domain/models/text/a_speech_text.py`
- Properties:
  - `id`: UUID
  - `speech_id`: UUID (foreign key to Speech)
  - `raw_text`: UUID (foreign key to RawText)
  - `language_code`: LanguageEnum
  - `clean_text`: Optional[UUID] (foreign key to CleanText)
  - `translated_text`: Optional[UUID] (foreign key to TranslatedText)
  - `sentences`: Optional[UUID] (foreign key to TextSentences)
  - `tokens`: Optional[UUID] (foreign key to TokenizedText)
  - `ngram_tokens`: Optional[UUID] (foreign key to NGramizedText)
  - `text_metrics`: Optional[TextMetrics]

### Text Processing Entities

#### RawText (Entity)
**File**: `src/domain/models/text/e_text_raw.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `text`: str - original text content
- Methods: `num_characters()`

#### CleanText (Entity)
**File**: `src/domain/models/text/e_text_clean.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `text`: str - cleaned text content
- Methods: `num_words()`, `num_characters()`, `num_sentences()`, `split_sentences()`

#### TranslatedText (Entity)
**File**: `src/domain/models/text/e_text_translated.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `translated_text`: str - English translation

#### TokenizedText (Entity)
**File**: `src/domain/models/text/e_text_tokenized.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `tokens`: List[str] - tokenized text
- Methods: `num_tokens()`, `unique_token_count()`

#### TextSentences (Entity)
**File**: `src/domain/models/text/e_text_split.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `sentences`: List[str] - sentence-split text

#### NGramizedText (Entity)
**File**: `src/domain/models/text/e_text_ngrams.py`
- Properties:
  - `id`: UUID
  - `speech_text_id`: UUID
  - `tokens`: List[str] - n-gram tokens

#### MetricsPlugin (Entity)
**File**: `src/domain/models/text/e_speech_metrics_plugin.py`
- Properties:
  - `id`: UUID
  - `dominant_topics`: Optional[List[Dict[str, float]]] - topic modeling results
  - `sentiment`: Optional[Dict[str, float]] - sentiment analysis
  - `dynamic_codes`: Optional[List[Any]] - extensible metrics
- Methods: `set_dominant_topics()`, `add_dominant_topic()`

### Text Value Objects

#### ProtocolText
**File**: `src/domain/models/text/v_protocol_text.py`
- Properties: `protocol_text`: str
- Methods: `unique_character_list()`

#### PartyProgramText
**File**: `src/domain/models/text/v_party_program_text.py`
- Properties: `program_text`: str
- Represents political party program documents

#### Agenda
**File**: `src/domain/models/text/v_protocol_agenda.py`
- Properties: `items`: Dict[str, List[str]]
- Methods: `all_types()`
- Represents structured session agendas

#### TextMetrics
**File**: `src/domain/models/text/v_text_metrics.py`
- Properties:
  - `word_count`: Optional[int]
  - `character_count`: Optional[int]
  - `token_count`: Optional[int]
  - `unique_token_count`: Optional[int]
  - `sentence_count`: Optional[int]

## Common Domain

### Corpora (Aggregate Root)
**File**: `src/domain/models/common/a_corpora.py`
- Properties:
  - `id`: UUID
  - `label`: Label
  - `texts`: Set[UUID] - collection of speech texts
  - `countries`: Optional[List[UUID]] - filter by countries
  - `institutions`: Optional[List[UUID]] - filter by institutions
  - `protocols`: Optional[List[UUID]] - filter by protocols
  - `parties`: Optional[List[UUID]] - filter by parties
  - `speakers`: Optional[List[UUID]] - filter by speakers
  - `periods`: Optional[List[UUID]] - filter by time periods
- Represents curated collections of texts for analysis

## Domain Relationships

### Core Aggregates
1. **Country** → contains Institutions, Parties, Speakers, Periods
2. **Protocol** → contains Speeches, belongs to Institution
3. **SpeechText** → contains various text processing entities
4. **Corpora** → references collections of entities for analysis

### Key Relationships
- Country ←→ Institution (one-to-many)
- Country ←→ Party (one-to-many)
- Country ←→ Speaker (one-to-many)
- Institution ←→ Protocol (one-to-many)
- Protocol ←→ Speech (one-to-many)
- Speaker ←→ Speech (one-to-many)
- Speech ←→ SpeechText (one-to-one)
- Party ←→ Speaker (one-to-many, optional)

## Design Patterns and Principles

### Domain-Driven Design
- Clear aggregate boundaries
- Entities have identity, Value Objects are immutable
- Rich domain model with business logic
- Repository pattern for data access abstraction

### Extensibility
- MetadataPlugin for dynamic properties
- MetricsPlugin for analytical extensions
- Enum-based type safety
- Optional relationships for flexibility

### Text Processing Pipeline
- Raw → Clean → Tokenized → Translated
- Sentence splitting and n-gram generation
- Metrics collection and topic modeling
- Immutable text transformations

This domain model supports comprehensive parliamentary discourse analysis while maintaining clean boundaries and extensibility for future requirements.