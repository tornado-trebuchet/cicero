import typer

from backend.application.modules.text_services.extractor.extractor import ExtractorService
from backend.application.modules.text_services.extractor.extractor_spec import ExtractionSpec
from backend.domain.models.common.v_common import UUID
from backend.domain.models.common.v_enums import (
    CountryEnum,
    InstitutionTypeEnum,
    LanguageEnum,
    ProtocolTypeEnum
)

app = typer.Typer(help="Speech extraction commands")


@app.command("speeches")
def extract_speeches(
    protocol_id: str = typer.Argument(..., help="Protocol ID to extract speeches from"),
    country: str = typer.Option(
        "GERMANY",
        "--country", "-c",
        help="Country enum value (default: GERMANY)"
    ),
    institution: str = typer.Option(
        "PARLIAMENT",
        "--institution", "-i",
        help="Institution type enum value (default: PARLIAMENT)"
    ),
    language: str = typer.Option(
        "DE",
        "--language", "-l",
        help="Language enum value (default: DE)"
    ),
    protocol_type: str = typer.Option(
        "PLENARY",
        "--protocol-type", "-t",
        help="Protocol type enum value (default: PLENARY)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Extract speeches from a protocol.
    
    Examples:
        cicero extract speeches abc-123-def --verbose
        cicero extract speeches abc-123-def --country GERMANY --institution PARLIAMENT
    """
    
    try:
        # Build extraction spec
        typer.echo(f"🗣️  Extracting speeches from protocol: {protocol_id}")
        
        if verbose:
            typer.echo(f"Configuration:")
            typer.echo(f"  Country: {country}")
            typer.echo(f"  Institution: {institution}")
            typer.echo(f"  Language: {language}")
            typer.echo(f"  Protocol Type: {protocol_type}")
        
        extraction_spec = ExtractionSpec(
            protocol=UUID(protocol_id),
            country=CountryEnum(country),
            institution=InstitutionTypeEnum(institution),
            language=LanguageEnum(language),
            protocol_type=ProtocolTypeEnum(protocol_type),
            pattern_spec=None
        )
        
        # Execute extraction
        extractor = ExtractorService()
        speeches = extractor.extract_speeches(extraction_spec)
        
        typer.echo(f"✅ Successfully extracted {len(speeches)} speeches")
        
        if verbose:
            typer.echo("Speech IDs:")
            for speech in speeches[:5]:  # Show first 5
                typer.echo(f"  • {speech.id.value}")
            if len(speeches) > 5:
                typer.echo(f"  ... and {len(speeches) - 5} more")
        
    except ValueError as e:
        typer.echo(f"❌ Extraction failed: {str(e)}", err=True)
        typer.echo("💡 Tip: Make sure the protocol exists and doesn't already have speeches", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to extract speeches: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
