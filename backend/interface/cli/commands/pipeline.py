import typer
from pathlib import Path
from typing import Optional
import time

from backend.interface.cli.config.cli_config import ConfigLoader
from backend.interface.cli.config.converters import ConfigConverter
from backend.application.pipeline.spec import PipelineResult

app = typer.Typer(help="Pipeline orchestration commands")

DEFAULT_CONFIG_DIR = Path(__file__).parent.parent / "config" / "presets"


@app.command("run")
def run_pipeline(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to pipeline configuration file (YAML/JSON)"
    ),
    preset: Optional[str] = typer.Option(
        None,
        "--preset", "-p", 
        help="Use predefined preset: full, fetch-extract, extract-preprocess, preprocess-model, custom"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Run a complete pipeline based on configuration.
    
    Examples:
        cicero pipeline run --preset full
        cicero pipeline run --config /path/to/config.yaml
        cicero pipeline run --preset fetch-extract --verbose
    """
    from backend.application.pipeline.controller import Pipeline
    
    # Determine config file
    if config_file and preset:
        typer.echo("Error: Cannot specify both --config and --preset", err=True)
        raise typer.Exit(1)
        
    if not config_file and not preset:
        typer.echo("Error: Must specify either --config or --preset", err=True)
        raise typer.Exit(1)
    
    if preset:
        preset_map = {
            "full": "full_pipeline.yaml",
            "fetch-extract": "fetch_extract.yaml", 
            "extract-preprocess": "extract_preprocess.yaml",
            "preprocess-model": "preprocess_model.yaml",
            "custom": "custom_pipeline.yaml"
        }
        
        if preset not in preset_map:
            typer.echo(f"Error: Unknown preset '{preset}'. Available: {', '.join(preset_map.keys())}", err=True)
            raise typer.Exit(1)
            
        config_file = DEFAULT_CONFIG_DIR / preset_map[preset]
    
    # At this point config_file is definitely not None
    assert config_file is not None
    
    if not config_file.exists():
        typer.echo(f"Error: Configuration file not found: {config_file}", err=True)
        raise typer.Exit(1)
    
    try:
        # Load and convert configuration
        typer.echo(f"📋 Loading configuration from: {config_file}")
        cli_config = ConfigLoader.load_pipeline_config(config_file)
        pipeline_spec = ConfigConverter.cli_pipeline_to_spec(cli_config)
        
        if verbose:
            typer.echo(f"Pipeline type: {pipeline_spec.config.pipeline_type.value}")
            if pipeline_spec.config.steps:
                steps = [step.value for step in pipeline_spec.config.steps]
                typer.echo(f"Steps: {' -> '.join(steps)}")
        
        # Initialize and run pipeline
        typer.echo("🚀 Starting pipeline execution...")
        start_time = time.time()
        
        pipeline = Pipeline()
        result = pipeline.execute(pipeline_spec)
        
        # Display results
        _display_pipeline_result(result, verbose)
        
        # Final status
        execution_time = time.time() - start_time
        if result.success:
            typer.echo(f"✅ Pipeline completed successfully in {execution_time:.2f}s")
        else:
            typer.echo(f"❌ Pipeline failed after {execution_time:.2f}s")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"❌ Pipeline execution failed: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


@app.command("list-presets")
def list_presets():
    """List available pipeline presets"""
    
    presets = {
        "full": "Complete pipeline: Fetch → Extract → Preprocess → Model",
        "fetch-extract": "Fetch protocols and extract speeches only",
        "extract-preprocess": "Extract speeches from existing protocols and preprocess",
        "preprocess-model": "Preprocess existing speeches and run topic modeling",
        "custom": "Custom pipeline with user-defined steps"
    }
    
    typer.echo("📋 Available Pipeline Presets:")
    typer.echo()
    
    for preset, description in presets.items():
        typer.echo(f"  {preset:<20} {description}")
    
    typer.echo()
    typer.echo("Usage: cicero pipeline run --preset <preset_name>")


def _display_pipeline_result(result: PipelineResult, verbose: bool = False):
    """Display pipeline execution results"""
    
    typer.echo()
    typer.echo("📊 Pipeline Results:")
    typer.echo(f"   Type: {result.pipeline_type.value}")
    typer.echo(f"   Success: {'✅' if result.success else '❌'}")
    
    if result.steps_executed:
        executed_steps = [step.value for step in result.steps_executed]
        typer.echo(f"   Steps executed: {' -> '.join(executed_steps)}")
    
    if result.steps_failed:
        failed_steps = [step.value for step in result.steps_failed]
        typer.echo(f"   Steps failed: {', '.join(failed_steps)}")
    
    if result.execution_time_seconds:
        typer.echo(f"   Execution time: {result.execution_time_seconds:.2f}s")
    
    # Display step-specific results
    if verbose and result.success:
        if result.fetched_protocols:
            typer.echo(f"   📥 Protocols fetched: {len(result.fetched_protocols)}")
        
        if result.extracted_speeches:
            typer.echo(f"   🗣️  Speeches extracted: {len(result.extracted_speeches)}")
        
        if result.preprocessed_speeches:
            typer.echo(f"   🔧 Speeches preprocessed: {len(result.preprocessed_speeches)}")
        
        if result.final_corpora_id:
            typer.echo(f"   📚 Final corpora ID: {result.final_corpora_id.value}")
    
    # Display errors
    if result.error_messages:
        typer.echo()
        typer.echo("❌ Errors:")
        for error in result.error_messages:
            typer.echo(f"   • {error}")
    
    # Display warnings
    if result.warnings:
        typer.echo()
        typer.echo("⚠️  Warnings:")
        for warning in result.warnings:
            typer.echo(f"   • {warning}")


if __name__ == "__main__":
    app()
