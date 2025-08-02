# Cicero CLI

Command-line interface for the Cicero parliamentary data processing pipeline.

## Overview

The Cicero CLI provides comprehensive tools for processing parliamentary data through a sophisticated pipeline system. The main workflow involves:

1. **Fetching** protocols from external APIs
2. **Extracting** speeches from protocols  
3. **Preprocessing** text (cleaning, tokenization)
4. **Modeling** (topic modeling, analysis)

## Quick Start

### 1. Seed Default Data (Required First)
```bash
# This populates the database with countries, institutions, etc.
python -m backend.interface.cli.typer data seed --yes
```

### 2. Run a Complete Pipeline
```bash
# Run full pipeline with default German parliament settings
python -m backend.interface.cli.typer pipeline run --preset full

# Run fetch and extract only
python -m backend.interface.cli.typer pipeline run --preset fetch-extract
```

### 3. Create and Manage Corpora
```bash
# Create a corpora for analysis
python -m backend.interface.cli.typer corpora create --preset german-2023

# List all corpora
python -m backend.interface.cli.typer corpora list

# Get detailed info about a corpora
python -m backend.interface.cli.typer corpora get <corpora-id>
```

## Command Structure

### Pipeline Commands
- `pipeline run --preset <preset>` - Run complete pipelines
- `pipeline run --config <file>` - Run with custom configuration
- `pipeline list-presets` - Show available presets

### Individual Step Commands
- `fetch protocols --preset <preset>` - Fetch protocols
- `extract speeches <protocol-id>` - Extract speeches from protocol
- `preprocess speeches "<speech-ids>"` - Preprocess text
- `model topic-model <corpora-id>` - Run topic modeling

### Corpora Management
- `corpora create --preset <preset>` - Create corpora
- `corpora list` - List all corpora
- `corpora get <id>` - Get corpora details
- `corpora delete <id>` - Delete corpora (with confirmation)

### Data Management
- `data seed` - Seed default data (requires confirmation)

## Configuration

The CLI uses YAML/JSON configuration files. Sample configurations are provided in:
```
backend/interface/cli/config/presets/
```

### Available Presets

**Pipeline Presets:**
- `full` - Complete pipeline: Fetch → Extract → Preprocess → Model
- `fetch-extract` - Fetch protocols and extract speeches only
- `extract-preprocess` - Extract speeches and preprocess text
- `preprocess-model` - Preprocess text and run modeling
- `custom` - Custom pipeline with user-defined steps

**Fetcher Presets:**
- `single` - Fetch a single protocol
- `batch` - Fetch multiple protocols

**Corpora Presets:**
- `german-2023` - German Parliament 2023 data

## Examples

### Complete Workflow
```bash
# 1. Seed the database
python -m backend.interface.cli.typer data seed --yes

# 2. Run a full pipeline
python -m backend.interface.cli.typer pipeline run --preset full --verbose

# 3. List created corpora
python -m backend.interface.cli.typer corpora list

# 4. Run additional analysis on existing corpora
python -m backend.interface.cli.typer model topic-model <corpora-id>
```

### Step-by-Step Processing
```bash
# 1. Fetch some protocols
python -m backend.interface.cli.typer fetch protocols --preset batch --limit 3

# 2. Extract speeches from a specific protocol
python -m backend.interface.cli.typer extract speeches <protocol-id> --verbose

# 3. Preprocess the extracted speeches
python -m backend.interface.cli.typer preprocess speeches "<speech-id-1>,<speech-id-2>"

# 4. Create a custom corpora
python -m backend.interface.cli.typer corpora create --countries <country-id> --label "My Analysis"
```

### Custom Configuration
```bash
# Create custom pipeline config
cat > my_pipeline.yaml << EOF
pipeline_type: "CUSTOM"
steps:
  - "FETCH"
  - "EXTRACT"
save_intermediate_results: true
output_corpora_label: "My Custom Analysis"

fetcher:
  server_base: "https://search.dip.bundestag.de"
  endpoint_spec: "/api/v1/plenarprotokoll"
  params:
    limit: 2

extraction:
  country: "GERMANY"
  institution: "PARLIAMENT"
  language: "DE"
  protocol_type: "PLENARY"
EOF

# Run with custom config
python -m backend.interface.cli.typer pipeline run --config my_pipeline.yaml
```

## Error Handling

The CLI provides detailed error messages and suggestions. Use `--verbose` for full stack traces during debugging.

Common issues:
- **Missing default data**: Run `data seed` first
- **Protocol not found**: Check that the protocol ID exists
- **Speeches already exist**: Extraction is idempotent per protocol
- **Invalid UUIDs**: Ensure UUIDs are valid and exist in the database

## Configuration Files

Sample configuration files are provided for all components. You can copy and modify these for your specific needs:

- Pipeline configs: `presets/full_pipeline.yaml`, etc.
- Fetcher configs: `presets/fetcher_batch.yaml`, etc.  
- Corpora specs: `presets/corpora_german_2023.yaml`, etc.

## Development Notes

The CLI maintains strict layer boundaries:
- Uses existing application use cases
- Leverages dependency injection where available
- Converts CLI configs to application specs
- Provides progress reporting without data exports
