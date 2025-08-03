import typer
from pathlib import Path
from typing import Optional

from backend.interface.cli.config.cli_config import ConfigLoader
from backend.interface.cli.config.converters import ConfigConverter
from backend.application.use_cases.common.corpora import CorporaManger
from backend.application.use_cases.common.corpora_spec import CorporaSpec
from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from backend.infrastructure.repository.pgsql.common.rep_joint_q import JointQRepository
from backend.infrastructure.repository.pgsql.context.rep_period import PeriodRepository
from backend.infrastructure.repository.pgsql.text.rep_text_raw import RawTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_tokenized import TokenizedTextRepository
from backend.infrastructure.repository.pgsql.text.rep_text_ngrams import NGramizedTextRepository
from backend.domain.models.common.v_common import UUID
from backend.domain.models.context.v_label import Label

app = typer.Typer(help="Corpora management commands")

DEFAULT_CONFIG_DIR = Path(__file__).parent.parent / "config" / "presets"


@app.command("create")
def create_corpora(
    config_file: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to corpora specification file (YAML/JSON)"
    ),
    preset: Optional[str] = typer.Option(
        None,
        "--preset", "-p",
        help="Use predefined preset: german-2023"
    ),
    countries: Optional[str] = typer.Option(
        None,
        "--countries",
        help="Comma-separated list of country UUIDs"
    ),
    institutions: Optional[str] = typer.Option(
        None,
        "--institutions", 
        help="Comma-separated list of institution UUIDs"
    ),
    periods: Optional[str] = typer.Option(
        None,
        "--periods",
        help="Comma-separated list of period UUIDs"
    ),
    parties: Optional[str] = typer.Option(
        None,
        "--parties",
        help="Comma-separated list of party UUIDs"
    ),
    speakers: Optional[str] = typer.Option(
        None,
        "--speakers",
        help="Comma-separated list of speaker UUIDs"
    ),
    protocols: Optional[str] = typer.Option(
        None,
        "--protocols",
        help="Comma-separated list of protocol UUIDs"
    ),
    label: Optional[str] = typer.Option(
        None,
        "--label", "-l",
        help="Label for the corpora"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Create a new corpora collection based on filter criteria.
    
    Examples:
        cicero corpora create --preset german-2023
        cicero corpora create --config /path/to/corpora_spec.yaml
        cicero corpora create --countries uuid1,uuid2 --label "My Analysis"
    """
    
    try:
        # Determine corpora spec
        if config_file and preset:
            typer.echo("Error: Cannot specify both --config and --preset", err=True)
            raise typer.Exit(1)
        
        if config_file and (countries or institutions or periods or parties or speakers or protocols):
            typer.echo("Error: Cannot specify both --config and individual filter options", err=True)
            raise typer.Exit(1)
        
        if preset and (countries or institutions or periods or parties or speakers or protocols):
            typer.echo("Error: Cannot specify both --preset and individual filter options", err=True)
            raise typer.Exit(1)
        
        corpora_spec = None
        
        if config_file:
            if not config_file.exists():
                typer.echo(f"Error: Configuration file not found: {config_file}", err=True)
                raise typer.Exit(1)
            
            typer.echo(f"📋 Loading corpora spec from: {config_file}")
            cli_config = ConfigLoader.load_corpora_spec_config(config_file)
            corpora_spec = ConfigConverter.cli_corpora_spec_to_spec(cli_config)
            
        elif preset:
            preset_map = {
                "german-2023": "corpora_german_2023.yaml"
            }
            
            if preset not in preset_map:
                typer.echo(f"Error: Unknown preset '{preset}'. Available: {', '.join(preset_map.keys())}", err=True)
                raise typer.Exit(1)
            
            preset_file = DEFAULT_CONFIG_DIR / preset_map[preset]
            if not preset_file.exists():
                typer.echo(f"Error: Preset file not found: {preset_file}", err=True)
                raise typer.Exit(1)
            
            typer.echo(f"📋 Loading preset: {preset}")
            cli_config = ConfigLoader.load_corpora_spec_config(preset_file)
            corpora_spec = ConfigConverter.cli_corpora_spec_to_spec(cli_config)
            
        else:
            # Build from individual options
            
            country_uuids = None
            if countries:
                country_uuids = [UUID(c.strip()) for c in countries.split(",")]
            
            institution_uuids = None
            if institutions:
                institution_uuids = [UUID(i.strip()) for i in institutions.split(",")]
            
            period_uuids = None
            if periods:
                period_uuids = [UUID(p.strip()) for p in periods.split(",")]
            
            party_uuids = None
            if parties:
                party_uuids = [UUID(p.strip()) for p in parties.split(",")]
            
            speaker_uuids = None
            if speakers:
                speaker_uuids = [UUID(s.strip()) for s in speakers.split(",")]
            
            protocol_uuids = None
            if protocols:
                protocol_uuids = [UUID(p.strip()) for p in protocols.split(",")]
            
            corpora_spec = CorporaSpec(
                countries=country_uuids,
                institutions=institution_uuids,
                periods=period_uuids,
                parties=party_uuids,
                speakers=speaker_uuids,
                protocols=protocol_uuids
            )
        
        if not corpora_spec:
            typer.echo("Error: No corpora specification provided", err=True)
            raise typer.Exit(1)
        
        # Initialize corpora manager
        corpora_manager = _get_corpora_manager()
        
        # Create corpora
        typer.echo("🏗️  Creating corpora...")
        corpora = corpora_manager.assemble_corpora(corpora_spec)
        
        # Update label if provided
        if label:
            corpora.label = Label(label)
            corpora_manager.corpora_repo.update(corpora)
        
        if verbose:
            typer.echo(f"   Corpora ID: {corpora.id.value}")
            typer.echo(f"   Label: {corpora.label.value}")
            typer.echo(f"   Number of texts: {len(corpora.texts)}")
            if corpora.countries:
                typer.echo(f"   Countries: {len(corpora.countries)}")
            if corpora.institutions:
                typer.echo(f"   Institutions: {len(corpora.institutions)}")
            if corpora.periods:
                typer.echo(f"   Periods: {len(corpora.periods)}")
        
        typer.echo(f"✅ Corpora created successfully!")
        typer.echo(f"📚 Corpora ID: {corpora.id.value}")
        typer.echo(f"🏷️  Label: {corpora.label.value}")
        typer.echo(f"📄 Total texts: {len(corpora.texts)}")
        
    except Exception as e:
        typer.echo(f"❌ Failed to create corpora: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


@app.command("list")
def list_corpora(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """List all corpora in the system"""
    
    try:
        corpora_manager = _get_corpora_manager()
        all_corpora = corpora_manager.corpora_repo.list()
        
        if not all_corpora:
            typer.echo("📚 No corpora found")
            return
        
        typer.echo(f"📚 Found {len(all_corpora)} corpora:")
        typer.echo()
        
        for corpora in all_corpora:
            typer.echo(f"🔹 {corpora.label.value}")
            typer.echo(f"   ID: {corpora.id.value}")
            typer.echo(f"   Texts: {len(corpora.texts)}")
            
            if verbose:
                if corpora.countries:
                    typer.echo(f"   Countries: {len(corpora.countries)}")
                if corpora.institutions:
                    typer.echo(f"   Institutions: {len(corpora.institutions)}")
                if corpora.periods:
                    typer.echo(f"   Periods: {len(corpora.periods)}")
                if corpora.parties:
                    typer.echo(f"   Parties: {len(corpora.parties)}")
                if corpora.speakers:
                    typer.echo(f"   Speakers: {len(corpora.speakers)}")
            
            typer.echo()
            
    except Exception as e:
        typer.echo(f"❌ Failed to list corpora: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command("get")
def get_corpora(
    corpora_id: str = typer.Argument(..., help="Corpora ID"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Get detailed information about a specific corpora"""
    
    try:
        corpora_manager = _get_corpora_manager()
        corpora = corpora_manager.get_corpora_by_id(UUID(corpora_id))
        
        typer.echo(f"📚 Corpora: {corpora.label.value}")
        typer.echo(f"   ID: {corpora.id.value}")
        typer.echo(f"   Total texts: {len(corpora.texts)}")
        
        if corpora.countries:
            typer.echo(f"   Countries ({len(corpora.countries)}):")
            for country_id in corpora.countries:
                typer.echo(f"     • {country_id.value}")
        
        if corpora.institutions:
            typer.echo(f"   Institutions ({len(corpora.institutions)}):")
            for inst_id in corpora.institutions:
                typer.echo(f"     • {inst_id.value}")
        
        if corpora.periods:
            typer.echo(f"   Periods ({len(corpora.periods)}):")
            for period_id in corpora.periods:
                typer.echo(f"     • {period_id.value}")
        
        if corpora.parties:
            typer.echo(f"   Parties ({len(corpora.parties)}):")
            for party_id in corpora.parties:
                typer.echo(f"     • {party_id.value}")
        
        if corpora.speakers:
            typer.echo(f"   Speakers ({len(corpora.speakers)}):")
            for speaker_id in corpora.speakers:
                typer.echo(f"     • {speaker_id.value}")
        
        if verbose:
            typer.echo(f"   Text IDs ({len(corpora.texts)}):")
            for text_id in corpora.texts:
                typer.echo(f"     • {text_id.value}")
                
    except Exception as e:
        typer.echo(f"❌ Failed to get corpora: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command("delete")
def delete_corpora(
    corpora_id: str = typer.Argument(..., help="Corpora ID"),
    confirm: bool = typer.Option(
        False, 
        "--yes", "-y", 
        help="Skip confirmation prompt"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Delete a corpora (DANGEROUS - requires confirmation)"""
    
    try:
        corpora_manager = _get_corpora_manager()
        
        # Get corpora details first
        corpora = corpora_manager.get_corpora_by_id(UUID(corpora_id))
        
        typer.echo(f"🗑️  About to delete corpora:")
        typer.echo(f"   ID: {corpora.id.value}")
        typer.echo(f"   Label: {corpora.label.value}")
        typer.echo(f"   Texts: {len(corpora.texts)}")
        
        if not confirm:
            delete_confirmed = typer.confirm(
                "⚠️  Are you sure you want to delete this corpora? This action cannot be undone!"
            )
            if not delete_confirmed:
                typer.echo("❌ Deletion cancelled")
                return
        
        # Delete corpora
        corpora_manager.corpora_repo.delete(UUID(corpora_id))
        
        typer.echo(f"✅ Corpora deleted successfully")
        
    except Exception as e:
        typer.echo(f"❌ Failed to delete corpora: {str(e)}", err=True)
        raise typer.Exit(1)


def _get_corpora_manager() -> CorporaManger:
    """Initialize and return a CorporaManger with all dependencies"""
    return CorporaManger(
        corpora_repo=CorporaRepository(),
        joint_q_repo=JointQRepository(),
        period_repo=PeriodRepository(),
        raw_text_repo=RawTextRepository(),
        clean_text_repo=CleanTextRepository(),
        tokenized_text_repo=TokenizedTextRepository(),
        ngramized_text_repo=NGramizedTextRepository(),
    )


if __name__ == "__main__":
    app()
