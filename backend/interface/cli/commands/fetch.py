import typer
from pathlib import Path
from typing import Optional

from backend.interface.cli.config.cli_config import ConfigLoader
from backend.interface.cli.config.converters import ConfigConverter
from backend.application.di import di_service

app = typer.Typer(help="Data fetching commands")

DEFAULT_CONFIG_DIR = Path(__file__).parent.parent / "config" / "presets"


@app.command("protocols")
def fetch_protocols(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to fetcher configuration file (YAML/JSON)"
    ),
    preset: Optional[str] = typer.Option(
        None,
        "--preset", "-p",
        help="Use predefined preset: single, batch"
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit", "-l",
        help="Maximum number of protocols to fetch"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Fetch protocols from external APIs.
    
    Examples:
        cicero fetch protocols --preset batch --limit 5
        cicero fetch protocols --config /path/to/fetcher.yaml
    """
    
    try:
        # Determine config
        if config_file and preset:
            typer.echo("Error: Cannot specify both --config and --preset", err=True)
            raise typer.Exit(1)
        
        if not config_file and not preset:
            typer.echo("Error: Must specify either --config or --preset", err=True)
            raise typer.Exit(1)
        
        if preset:
            preset_map = {
                "single": "fetcher_single.yaml",
                "batch": "fetcher_batch.yaml"
            }
            
            if preset not in preset_map:
                typer.echo(f"Error: Unknown preset '{preset}'. Available: {', '.join(preset_map.keys())}", err=True)
                raise typer.Exit(1)
            
            config_file = DEFAULT_CONFIG_DIR / preset_map[preset]
        
        assert config_file is not None
        
        if not config_file.exists():
            typer.echo(f"Error: Configuration file not found: {config_file}", err=True)
            raise typer.Exit(1)
        
        # Load config and create spec
        typer.echo(f"📋 Loading fetcher config from: {config_file}")
        
        # Load as pipeline config to get the fetcher section
        cli_config = ConfigLoader.load_pipeline_config(config_file)
        if not cli_config.fetcher:
            typer.echo("Error: No fetcher configuration found in file", err=True)
            raise typer.Exit(1)
        
        # Override limit if provided
        if limit:
            if cli_config.fetcher.params is None:
                cli_config.fetcher.params = {}
            cli_config.fetcher.params["limit"] = limit
        
        fetcher_spec = ConfigConverter.cli_fetcher_to_spec(cli_config.fetcher)
        
        if verbose:
            typer.echo(f"Fetcher config:")
            typer.echo(f"  Server: {fetcher_spec.server_base}")
            typer.echo(f"  Endpoint: {fetcher_spec.endpoint_spec}")
            if fetcher_spec.params and "limit" in fetcher_spec.params:
                typer.echo(f"  Limit: {fetcher_spec.params['limit']}")
        
        # Execute fetching
        typer.echo("📥 Fetching protocols...")
        
        fetcher = di_service.get_bundestag_fetcher(fetcher_spec)
        
        if hasattr(fetcher, 'fetch_list'):
            protocol_ids = fetcher.fetch_list()
            typer.echo(f"✅ Successfully fetched {len(protocol_ids)} protocols")
            
            if verbose:
                typer.echo("Protocol IDs:")
                for pid in protocol_ids[:5]:  # Show first 5
                    typer.echo(f"  • {pid.value}")
                if len(protocol_ids) > 5:
                    typer.echo(f"  ... and {len(protocol_ids) - 5} more")
        else:
            protocol = fetcher.fetch_single()
            typer.echo(f"✅ Successfully fetched 1 protocol")
            if verbose:
                typer.echo(f"Protocol ID: {protocol.id.value}")
        
    except Exception as e:
        typer.echo(f"❌ Failed to fetch protocols: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
