# Application Data Flow Documentation

This document outlines the data transformation flows throughout the Cicero application via the mapper pattern. It covers all transformations where DTO/Domain objects change state during processing.

## Data Transformation Layers

The application employs a multi-layered data transformation architecture with three primary transformation boundaries:

1. **Infrastructure Layer**: Domain ↔ ORM transformations
2. **Interface Layer**: Domain ↔ API DTO transformations  
3. **Service Layer**: Domain ↔ Service DTO transformations

## Infrastructure Layer Transformations (Domain ↔ ORM)

### Common Domain Transformations

#### Corpora Mapper (`src/infrastructure/mappers/common/m_corpora.py`)
- **Domain → ORM**: `CorporaMapper.to_orm()`
  - Transforms `Corpora` domain aggregate to `CorporaORM`
  - Extracts UUID values from domain objects
  - Converts collections to UUID lists
- **ORM → Domain**: `CorporaMapper.to_domain()`
  - Reconstructs `Corpora` from `CorporaORM`
  - Creates UUID value objects from raw UUIDs
  - Rebuilds domain relationships

### Context Domain Transformations

#### Country Mapper (`src/infrastructure/mappers/context/m_country.py`)
- **Domain → ORM**: `CountryMapper.to_orm()`
  - Maps `Country` aggregate to `CountryORM`
  - Extracts country enum and ID values
- **ORM → Domain**: `CountryMapper.to_domain()`
  - Reconstructs `Country` with related entity UUIDs
  - Maps associated institutions, periods, parties, speakers

#### Institution Mapper (`src/infrastructure/mappers/context/m_institution.py`)
- **Domain → ORM**: `InstitutionMapper.to_orm()`
  - Transforms `Institution` entity to `InstitutionORM`
  - Serializes metadata plugin to JSON properties
- **ORM → Domain**: `InstitutionMapper.to_domain()`
  - Reconstructs institution with metadata plugin
  - Maps related protocols and periods

#### Party Mapper (`src/infrastructure/mappers/context/m_party.py`)
- **Domain → ORM**: `PartyMapper.to_orm()`
  - Maps `Party` entity to `PartyORM`
  - Extracts party program text
- **ORM → Domain**: `PartyMapper.to_domain()`
  - Reconstructs party with program text value object
  - Maps member speakers

#### Period Mapper (`src/infrastructure/mappers/context/m_period.py`)
- **Domain → ORM**: `PeriodMapper.to_orm()`
  - Transforms `Period` entity to `PeriodORM`
  - Extracts date/time values from value objects
- **ORM → Domain**: `PeriodMapper.to_domain()`
  - Reconstructs period with DateTime value objects
  - Restores label value object

#### Speaker Mapper (`src/infrastructure/mappers/context/m_speaker.py`)
- **Domain → ORM**: `SpeakerMapper.to_orm()`
  - Maps `Speaker` entity to `SpeakerORM`
  - Extracts name, party, date values
- **ORM → Domain**: `SpeakerMapper.to_domain()`
  - Reconstructs speaker with value objects
  - Maps associated speeches and party

### Text Domain Transformations

#### Protocol Mapper (`src/infrastructure/mappers/text/m_protocol.py`)
- **Domain → ORM**: `ProtocolMapper.to_orm()`
  - Transforms `Protocol` aggregate to `ProtocolORM`
  - Serializes agenda and metadata to JSON
  - Extracts protocol text content
- **ORM → Domain**: `ProtocolMapper.to_domain()`
  - Reconstructs protocol with value objects
  - Deserializes agenda and metadata plugins

#### Speech Mapper (`src/infrastructure/mappers/text/m_speech.py`)
- **Domain → ORM**: `SpeechMapper.to_orm()`
  - Maps `Speech` aggregate to `SpeechORM`
  - Serializes metadata plugin via `_metadata_to_orm()`
- **ORM → Domain**: `SpeechMapper.to_domain()`
  - Reconstructs speech entity
  - Deserializes metadata via `_metadata_to_domain()`

#### Speech Text Mapper (`src/infrastructure/mappers/text/m_speech_text.py`)
- **Domain → ORM**: `SpeechTextMapper.to_orm()`
  - Transforms `SpeechText` aggregate to `SpeechTextORM`
  - Serializes text metrics via `_metrics_to_orm()`
- **ORM → Domain**: `SpeechTextMapper.to_domain()`
  - Reconstructs speech text with related entities
  - Deserializes metrics via `_metrics_to_domain()`

#### Speech Metrics Mapper (`src/infrastructure/mappers/text/m_speech_metrics.py`)
- **Domain → ORM**: `SpeechMetricsMapper.to_orm()`
  - Maps `MetricsPlugin` to `SpeechMetricsORM`
  - Preserves topic modeling and sentiment data
- **ORM → Domain**: `SpeechMetricsMapper.to_domain()`
  - Reconstructs metrics plugin from ORM

#### Text Processing Mappers
Multiple mappers handle text processing entities:

- **Raw Text**: `RawTextMapper` (`m_text_raw.py`)
- **Clean Text**: `CleanTextMapper` (`m_text_clean.py`)
- **Tokenized Text**: `TokenizedTextMapper` (`m_text_tokenized.py`)
- **NGramized Text**: `NGramizedTextMapper` (`m_text_ngrams.py`)
- **Text Sentences**: `TextSentencesMapper` (`m_text_split.py`)
- **Translated Text**: `TranslatedTextMapper` (`m_text_translated.py`)

Each follows the same pattern:
- **Domain → ORM**: Extracts entity ID and content
- **ORM → Domain**: Reconstructs entity with UUID value objects

## Interface Layer Transformations (Domain ↔ API DTOs)

### Common API Mappings (`src/interface/api/mappers/mp_common.py`)

#### Corpora Transformations
- **Domain → DTO**: `corpora_to_dto()`
  - Transforms `Corpora` to `CorporaDTO`
  - Extracts UUID values for serialization
- **DTO → Domain**: `dto_to_corpora()`
  - Reconstructs domain from API input
  - Creates UUID and Label value objects

#### Corpora Specification Transformations
- **Spec → DTO**: `corpora_spec_to_dto()`
  - Maps `CorporaSpec` to `CorporaSpecDTO`
- **DTO → Spec**: `dto_to_corpora_spec()`
  - Reconstructs specification from API input

### Context API Mappings (`src/interface/api/mappers/mp_context.py`)

#### Entity to DTO Transformations
- **Country**: `country_to_dto()` - Maps to `CountryDTO`
- **Institution**: `institution_to_dto()` - Maps to `InstitutionDTO`
- **Party**: `party_to_dto()` - Maps to `PartyDTO`
- **Period**: `period_to_dto()` - Maps to `PeriodDTO`
- **Speaker**: `speaker_to_dto()` - Maps to `SpeakerDTO`

All context mappers extract UUID values and handle optional relationships.

### Text API Mappings (`src/interface/api/mappers/mp_text.py`)

#### Text Entity Transformations
- **Protocol**: `protocol_to_dto()` - Maps to `ProtocolDTO`
- **Speech**: `speech_to_dto()` - Maps to `SpeechDTO`
- **Speech Text**: `speech_text_to_dto()` - Maps to `SpeechTextDTO`
- **Raw Text**: `raw_text_to_dto()` - Maps to `RawTextDTO`
- **Clean Text**: `clean_text_to_dto()` - Maps to `CleanTextDTO`

### Service API Mappings (`src/interface/api/mappers/mp_service.py`)

#### Specification Transformations
- **Protocol Spec**: `protocol_spec_to_dto()` / `dto_to_protocol_spec()`
- **Extraction Spec**: `dto_to_extraction_spec()`
- **Preprocessor Spec**: `preprocessor_spec_to_dto()` / `dto_to_preprocessor_spec()`

## Service Layer Transformations (Domain ↔ Service DTOs)

### Text Service DTOs (`src/domain/services/text/*/serv_*_dto.py`)

#### Extractor Service (`serv_extractor_dto.py`)
- **SpeakerDTO**: Intermediate representation for speaker extraction
- **RawTextDTO**: Raw text container for processing
- **SpeechDTO**: Composite DTO combining speaker and text data

#### Preprocessor Service (`serv_preprocessor_dto.py`)
- **CleanTextDTO**: Container for cleaned text output

#### Tokenizer Service (`serv_tokenizer_dto.py`)
- **TokenizedTextDTO**: Contains tokenized text results

#### Translator Service (`serv_translator_dto.py`)
- **TranslatedTextDTO**: Contains translation results

### External Integration Transformations

#### German Protocol Integration (`src/infrastructure/external/germany/protocol_dto.py`)
- **GermanResponseProtocolDTO**: External API response mapping
  - Transforms external German parliament API responses
  - Maps to internal domain protocols via repository layer

## Data Flow Patterns

### 1. Protocol Processing Flow
```
External API → GermanResponseProtocolDTO → Protocol (Domain) → ProtocolORM → Database
                                        ↓
                                    ProtocolDTO → API Response
```

### 2. Speech Extraction Flow
```
Protocol (Domain) → ExtractSpeakersFromProtocol → SpeechDTO → Speech (Domain) → SpeechORM
```

### 3. Text Processing Flow
```
RawText → CleanTextDTO → CleanText → TokenizedTextDTO → TokenizedText → NGramizedText
```

### 4. Corpora Assembly Flow
```
CorporaSpecDTO → CorporaSpec → CorporaManger → Corpora (Domain) → CorporaORM
```

## Key Transformation Points

### Router Level Transformations
- **Context Router**: Domain entities → Context DTOs
- **Text Router**: Text entities → Text DTOs  
- **Service Router**: Processing specs → Service DTOs
- **Common Router**: Corpora entities → Common DTOs

### Repository Level Transformations
- All repositories use infrastructure mappers for Domain ↔ ORM conversion
- Bidirectional transformations maintain data integrity
- UUID value objects consistently handled across layers

### Service Level Transformations
- Text services use specialized DTOs for intermediate processing
- External APIs use dedicated response DTOs
- Processing specifications mapped between API and domain layers

## Transformation Characteristics

### Consistency Patterns
- UUID extraction/reconstruction across all mappers
- Metadata serialization/deserialization via plugin pattern
- Optional relationship handling with null checks
- Value object reconstruction from primitive types

### Error Handling
- Transformations assume valid input (no validation in mappers)
- Null safety implemented via optional type handling
- UUID reconstruction may throw on invalid format

### Performance Considerations
- Single-pass transformations without intermediate allocations
- Collection transformations use list comprehensions
- Metadata serialization cached where possible

This documentation provides a comprehensive overview of all data transformation points in the Cicero application, enabling developers to understand the complete data flow and identify transformation responsibilities across architectural layers.
