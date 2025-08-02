"""
Text preprocessing commands
"""
import typer
from typing import List

from backend.application.modules.text_services.preprocessor.preprocessor import PreprocessTextService
from backend.application.modules.text_services.preprocessor.preprocessor_spec import PreprocessorSpec
from backend.domain.models.common.v_common import UUID

app = typer.Typer(help="Text preprocessing commands")


@app.command("speeches")
def preprocess_speeches(
    speech_ids: str = typer.Argument(..., help="Comma-separated list of speech IDs"),
    batch_size: int = typer.Option(
        5,
        "--batch-size", "-b",
        help="Number of speeches to process in parallel (default: 5)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Preprocess speeches (clean text).
    
    Examples:
        cicero preprocess speeches "uuid1,uuid2,uuid3"
        cicero preprocess speeches "uuid1,uuid2" --batch-size 2 --verbose
    """
    
    try:
        # Parse speech IDs
        speech_id_list = [UUID(sid.strip()) for sid in speech_ids.split(",")]
        
        typer.echo(f"🔧 Preprocessing {len(speech_id_list)} speeches")
        
        if verbose:
            typer.echo(f"Batch size: {batch_size}")
            typer.echo(f"Speech IDs:")
            for sid in speech_id_list[:5]:  # Show first 5
                typer.echo(f"  • {sid.value}")
            if len(speech_id_list) > 5:
                typer.echo(f"  ... and {len(speech_id_list) - 5} more")
        
        # Process speeches
        processed_count = 0
        failed_count = 0
        errors: List[str] = []
        
        for i, speech_id in enumerate(speech_id_list):
            try:
                if verbose:
                    typer.echo(f"Processing speech {i+1}/{len(speech_id_list)}: {speech_id.value}")
                
                spec = PreprocessorSpec(speech=speech_id)
                preprocessor = PreprocessTextService(spec)
                preprocessor.execute()
                
                processed_count += 1
                
            except Exception as e:
                failed_count += 1
                error_msg = f"Speech {speech_id.value}: {str(e)}"
                errors.append(error_msg)
                if verbose:
                    typer.echo(f"  ❌ Failed: {str(e)}")
        
        # Summary
        typer.echo(f"✅ Preprocessing completed!")
        typer.echo(f"   Processed: {processed_count}")
        if failed_count > 0:
            typer.echo(f"   Failed: {failed_count}")
            
            if errors and verbose:
                typer.echo("❌ Errors:")
                for error in errors:
                    typer.echo(f"   • {error}")
        
        if failed_count > 0 and processed_count == 0:
            raise typer.Exit(1)
        
    except ValueError as e:
        typer.echo(f"❌ Invalid input: {str(e)}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to preprocess speeches: {str(e)}", err=True)
        if verbose:
            import traceback
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
