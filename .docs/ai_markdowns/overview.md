# Purpose 

Cicero is a comprehensive CLI/web tool designed for parliamentary speech analysis, data storage, and representation. It enables researchers and analysts to:

- **Fetch and Process Parliamentary Data**: Automatically retrieve parliamentary protocols from external APIs (currently supports German Bundestag)
- **Extract Speeches**: Parse parliamentary protocols to extract individual speeches with speaker information, party affiliation, and metadata
- **Text Processing Pipeline**: Clean, tokenize, translate, and analyze textual content using NLP techniques
- **Topic Modeling**: Perform advanced topic modeling using BERT-based models to identify themes and patterns in speeches
- **Sentiment Analysis**: Analyze emotional content and sentiment patterns in political discourse
- **Data Storage and Retrieval**: Store processed data in a PostgreSQL database with complex querying capabilities
- **API Access**: Provide RESTful API endpoints for data access and processing operations

The system is particularly focused on German parliamentary data but is designed to be extensible to other countries and institutions.

# Architecture 

Cicero follows **Domain-Driven Design (DDD)** principles with **Clean Architecture** patterns, ensuring separation of concerns and maintainability.

## Core Architecture Layers

### 1. Domain Layer (`src/domain/`)
The heart of the application containing business logic and rules:

- **Aggregates**: 
  - `Country` - Top-level aggregate representing nations
  - `Protocol` - Parliamentary session documents
  - `Corpora` - Collections of texts for analysis

- **Entities**:
  - `Speech` - Individual parliamentary speeches
  - `Speaker` - Parliamentary representatives
  - `Institution` - Political institutions (parliaments, etc.)
  - `Party` - Political parties
  - `Period` - Time periods for data organization
  - `MetricsPlugin` - Speech analysis metrics

- **Value Objects**:
  - `UUID`, `DateTime`, `HttpUrl` - Common value types
  - `TextMetrics` - Text statistics and measurements
  - `Label`, `Name` - Domain-specific text values

- **Domain Services**:
  - Text extraction and processing services
  - Topic modeling using BERT
  - Text cleaning and tokenization

### 2. Application Layer (`src/application/`)
Orchestrates domain operations and use cases:

- **Use Cases**: Business operation implementations
- **Modules**: 
  - `fetchers/` - External data acquisition
  - `text_services/` - Text processing pipeline
  - `modellers/` - ML model services
- **Dependency Injection**: Service composition and configuration

### 3. Infrastructure Layer (`src/infrastructure/`)
Handles external concerns and technical implementations:

- **Database**: PostgreSQL with SQLAlchemy ORM
- **External APIs**: Integration with parliamentary data sources
- **Repositories**: Data persistence abstractions
- **Mappers**: Domain ↔ Infrastructure object translation

### 4. Interface Layer (`src/interface/`)
External communication interfaces:

- **REST API**: FastAPI-based web service
- **CLI**: Command-line interface (planned)
- **DTOs**: Data transfer objects for API communication

## Key Design Patterns

- **Repository Pattern**: Data access abstraction
- **Aggregate Pattern**: Consistency boundaries and transaction management
- **Mapper Pattern**: Clean separation between domain and infrastructure models
- **Dependency Injection**: Loose coupling and testability
- **CQRS-inspired**: Separate read/write operations for complex queries

# Tech Stack 

## Backend Framework
- **Python 3.12**: Core language
- **FastAPI**: Modern async web framework for REST API
- **Uvicorn**: ASGI server for development and production

## Database & Persistence
- **PostgreSQL**: Primary database for structured data
- **SQLAlchemy 2.0**: Modern ORM with async support
- **Psycopg2**: PostgreSQL adapter

## Machine Learning & NLP
- **BERTopic**: Advanced topic modeling framework
- **Sentence Transformers**: Multilingual sentence embeddings
- **spaCy**: Industrial-strength NLP library
- **UMAP**: Dimensionality reduction for topic modeling
- **HDBSCAN**: Hierarchical density-based clustering
- **PyTorch**: Deep learning framework backend
- **Gensim**: Topic modeling and text similarity

## Text Processing
- **Regex**: Pattern matching for text extraction
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **split-words**: Word segmentation utilities

## Development & Infrastructure
- **Poetry**: Dependency management and packaging
- **Docker & Docker Compose**: Containerization
- **pytest**: Testing framework
- **Black**: Code formatting
- **Rich**: Terminal formatting and progress bars
- **tqdm**: Progress bars
- **Typer**: CLI framework
- **python-dotenv**: Environment variable management

## External Integrations
- **Requests**: HTTP client for external APIs
- **German Bundestag API**: Parliamentary data source

## Deployment & Operations
- **Docker**: Container runtime
- **PostgreSQL 15**: Production database
- **Environment-based Configuration**: 12-factor app compliance

## Key Technical Features

### Text Processing Pipeline
1. **Fetching**: Retrieve documents from external APIs
2. **Extraction**: Parse documents to extract speeches using regex patterns
3. **Preprocessing**: Clean and normalize text data
4. **Tokenization**: Break text into processable units
5. **Translation**: Convert to English for analysis (optional)
6. **Analysis**: Apply ML models for topic modeling and sentiment analysis

### Database Design
- **Multi-tenant**: Support for multiple countries and institutions
- **Normalized Schema**: Efficient storage with proper relationships
- **JSON Fields**: Flexible metadata and configuration storage
- **Indexing**: Optimized queries for large datasets

### API Design
- **RESTful**: Standard HTTP methods and status codes
- **Async**: Non-blocking operations for better performance (planned)
- **Streaming**: Real-time progress updates for long-running operations (planned)
- **Pagination**: Cursor-based pagination for large result sets (planned)

### Extensibility
- **Plugin Architecture**: Configurable text processing modules
- **Multi-language Support**: Designed for multiple parliamentary systems
- **Modular Services**: Independent service components
- **Configuration-driven**: Environment-based settings
