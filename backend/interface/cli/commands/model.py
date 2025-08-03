import typer
import traceback

from backend.application.modules.modellers.topic_modeller.topic_spec import TopicModellerSpec
from backend.infrastructure.repository.pgsql.common.rep_corpora import CorporaRepository
from backend.infrastructure.repository.pgsql.text.rep_text_clean import CleanTextRepository
from backend.infrastructure.repository.pgsql.text.rep_speech_metrics import SpeechMetricsRepository
from backend.domain.models.common.v_common import UUID


app = typer.Typer(help="Modeling and analysis commands")


@app.command("topic-model")
def topic_model(
    corpora_id: str = typer.Argument(..., help="Corpora ID to run topic modeling on"),
    annotate: bool = typer.Option(
        True,
        "--annotate/--no-annotate",
        help="Whether to annotate speeches with topic assignments (default: True)"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Run topic modeling on a corpora.
    
    Examples:
        cicero model topic-model abc-123-def
        cicero model topic-model abc-123-def --no-annotate --verbose
    """
    from backend.application.modules.modellers.topic_modeller.topic_modeller import TopicModeller
    from backend.domain.services.modelling.topic_modeller_bert import TopicModeler
    
    try:
        typer.echo(f"🤖 Running topic modeling on corpora: {corpora_id}")
        
        # Initialize dependencies
        corpora_repo = CorporaRepository()
        clean_text_repo = CleanTextRepository()
        speech_metrics_repo = SpeechMetricsRepository()
        topic_modeler = TopicModeler()
        
        # Get corpora
        corpora = corpora_repo.get_by_id(UUID(corpora_id))
        if not corpora:
            typer.echo(f"❌ Corpora not found: {corpora_id}", err=True)
            raise typer.Exit(1)
        
        if verbose:
            typer.echo(f"Corpora: {corpora.label.value}")
            typer.echo(f"Texts: {len(corpora.texts)}")
        
        # Initialize topic modeller
        topic_modeller = TopicModeller(
            corpora_repo=corpora_repo,
            clean_text_repo=clean_text_repo,
            speech_metrics_repo=speech_metrics_repo,
            topic_modeler=topic_modeler
        )
        
        # Create spec and run modeling
        spec = TopicModellerSpec(corpora=corpora)
        
        if annotate:
            typer.echo("📝 Building model and annotating speeches...")
            result = topic_modeller.build_model_and_annotate(spec)
            typer.echo("✅ Topic modeling and annotation completed!")
        else:
            typer.echo("📊 Building topic model...")
            result = topic_modeller.build_model(spec)
            typer.echo("✅ Topic modeling completed!")
        
        # Display results
        if verbose and "topics" in result:
            topics = result["topics"]
            typer.echo(f"📊 Model Results:")
            typer.echo(f"   Topics found: {len(topics) if topics else 0}")
            
            if topics and len(topics) > 0:
                typer.echo("   Sample topics:")
                for i, topic in enumerate(topics[:3]):  # Show first 3 topics
                    typer.echo(f"     Topic {i+1}: {topic}")
        
        if annotate and verbose:
            typer.echo("📝 Speeches have been annotated with topic assignments")
        
    except Exception as e:
        typer.echo(f"❌ Failed to run topic modeling: {str(e)}", err=True)
        if verbose:
            typer.echo(f"Stack trace:\n{traceback.format_exc()}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
