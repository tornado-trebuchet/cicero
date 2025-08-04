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
