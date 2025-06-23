# cicero


A cli/web tool for parliamentary speech analysis, data storage and representation.  `


| Слой               | Роль                                    | Технологии                                     |
| ------------------ | --------------------------------------- | ---------------------------------------------
| **Presentation**   | HTTP-API, UI, CLI-команды               | FastAPI (+ Jinja2 / React), Typer                |
| **Orchestration**  | Запуски ETL- DAG’ов, планировщик        | Prefect|
| **Services**       | Crawling, ETL, NLP-модули, визуализация | Scrapy/Playwright, pandas, matplotlib              |
| **Domain**         | Чистые классы/функции с логикой анализа | pydantic, чистые функции                |
| **Infrastructure** | Хранилища и коммуникации                | PostgreSQL (+ PGVector)|


Бэклог
: 

Celery + Redis


# Domain model Tree Structure

State
 ├── id: UUID
 └── name: str

Institution
 ├── id: UUID
 ├── state_id: UUID
 ├── institution_type: InstitutionTypeEnum
 ├── periodisation: List[Period]
 └── metadata: InstitutionMetadataPlugin (JSONB)

Protocol
 ├── id: UUID
 ├── institution_id: UUID
 ├── period: UUID     
 ├── extension: ExtensionEnum
 ├── file_source: HttpUrl         # единый URL для загрузки
 ├── protocol_type: ProtocolTypeEnum
 ├── speech_regex: RegexPattern
 ├── date: DateTime
 └── metadata: ProtocolMetadataPlugin (JSONB)

Speech
 ├── id: UUID
 ├── protocol_id: UUID
 ├── author: Speaker
 ├── text: TextVO
 ├── metrics: MetricsPlugin (JSONB)
 └── metadata: SpeechMetadataPlugin (JSONB)

 RegexPattern
 ├── id: UUID
 ├── state: UUID                
 ├── institution: UUID
 ├── period: UUID         
 ├── pattern: str
 ├── description: str
 ├── version: int
 └── is_active: bool

Period
 ├── id: UUID
 ├── label: str
 ├── start_date: DateTime
 ├── end_date: DateTime
 └── description: str

 Speaker
 ├── id: UUID
 ├── name: str
 ├── party: PartyEnum
 ├── role: str
 ├── birth_date: date
 └── gender: GenderEnum

─── Value Objects & Plugins ───────────────────────────────────────────

TextVO
 ├── language_code: LanguageEnum
 ├── raw_text: str
 ├── clean_text: str
 ├── tokens: List[str]
 ├── ngram_tokens: List[str]
 └── word_count: int

MetricsPlugin (JSONB) - validated
 ├── dominant_topics: List[{ topic: float }]
 ├── sentiment: { value: float }
 └── dynamic_codes: List[Any] # will be added later

[Institution]MetadataPlugin, [Protocol]MetadataPlugin, [Speech]MetadataPlugin - loose basic validation (length)
 └── любые динамические параметры, специфичные для источника/обработки


Enums:

InstitutionTypeEnum: [PARLIAMENT, FEDERAL_ASSEMBLY]
ProtocolTypeEnum: [PLENARY, HEARING]
PartyEnum(): State[State.id], Enums[]
GenderEnum: [MALE, FEMALE, NR]
LanguageEnum: [DE:"german",FR:"french"]
ExtensionEnum: [XML, JSON, TXT, PDF]